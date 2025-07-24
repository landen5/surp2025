import json
import argparse
from urllib.parse import urlparse
from collections import Counter # Required for summarize_hosts
import ast
import uuid

# --- ANSI color codes for highlighting ---
class BColors:
    HIGHLIGHT = '\033[93m' # Bright Yellow text
    RESET = '\033[0m'     # Reset to default color

# --- All helper functions (generate_context_snippet, etc.) are unchanged ---
def generate_context_snippet(content, term, location_type):
    # (Unchanged)
    if location_type not in ["Request Body", "Response Body"]:
        return content.replace(term, f"{BColors.HIGHLIGHT}{term}{BColors.RESET}")
    parsed_data = None
    if isinstance(content, (dict, list)): parsed_data = content
    elif isinstance(content, str):
        try: parsed_data = json.loads(content)
        except json.JSONDecodeError:
            try: parsed_data = ast.literal_eval(content)
            except (ValueError, SyntaxError, MemoryError, TypeError): parsed_data = None
    if parsed_data:
        try: pretty_content = json.dumps(parsed_data, indent=2); lines = pretty_content.split('\n')
        except TypeError: lines = str(parsed_data).split('\n')
    else: lines = str(content).split('\n')
    snippet_lines = []; line_num_with_term = -1
    for i, line in enumerate(lines):
        if term in line: line_num_with_term = i; break
    if line_num_with_term != -1:
        start = max(0, line_num_with_term - 2); end = min(len(lines), line_num_with_term + 3)
        for i in range(start, end):
            current_line = lines[i]
            if i == line_num_with_term:
                highlighted_line = current_line.replace(term, f"{BColors.HIGHLIGHT}{term}{BColors.RESET}")
                prefix = "  > "; snippet_lines.append(f"{prefix}{highlighted_line}")
            else:
                prefix = "    "; snippet_lines.append(f"{prefix}{current_line}")
        return "\n".join(snippet_lines)
    return str(content).replace(term, f"{BColors.HIGHLIGHT}{term}{BColors.RESET}")

def find_data_occurrences(har_file_path, search_terms, filter_methods=None):
    # (Unchanged)
    try:
        with open(har_file_path, 'r', encoding='utf-8') as f: har_data = json.load(f)
    except Exception as e: print(f"Error reading or parsing HAR file: {e}"); return None
    all_findings = [];
    if filter_methods: filter_methods = [m.upper() for m in filter_methods]
    for entry in har_data.get('log', {}).get('entries', []):
        request = entry.get('request', {}); response = entry.get('response', {}); method = request.get('method', '').upper()
        if (not request) or (filter_methods and method not in filter_methods): continue
        url = request.get('url');
        if not url: continue
        hostname = urlparse(url).hostname
        found_in_entry = set()
        for term in search_terms:
            def add_finding(term, location, content, location_type):
                finding_key = (method, url, location, term)
                if finding_key not in found_in_entry:
                    snippet = generate_context_snippet(content, term, location_type)
                    all_findings.append({ "method": method, "url": url, "hostname": hostname, "search_term": term, "location": location, "context_snippet": snippet })
                    found_in_entry.add(finding_key)
            if term in url: add_finding(term, "URL", url, "URL")
            for header in request.get('headers', []):
                if term in header.get('value', ''): add_finding(term, f"Request Header ('{header.get('name')}')", f"{header.get('name')}: {header.get('value')}", "Header")
            if 'postData' in request and 'text' in request['postData']:
                body_content = request['postData']['text']
                if body_content and term in str(body_content): add_finding(term, "Request Body", body_content, "Request Body")
            if 'content' in response and 'text' in response['content']:
                response_content = response['content']['text']
                if response_content and term in str(response_content): add_finding(term, "Response Body", response_content, "Response Body")
    return all_findings

def generate_rules_file(findings_to_export, action_choice, filename, transform_map=None):
    # (Unchanged)
    METHOD_MAP = { 'GET': 0, 'POST': 1, 'PUT': 2, 'DELETE': 3, 'PATCH': 4, 'HEAD': 5, 'OPTIONS': 6 }
    rules = []
    for finding in findings_to_export:
        matchers = []
        if finding['method'] in METHOD_MAP:
            matchers.append({ "method": METHOD_MAP[finding['method']], "type": "method", "uiType": finding['method'] })
        matchers.append({ "type": "simple-path", "path": finding['url'] })
        if finding['location'] == 'Request Body':
            matchers.append({"type": "raw-body-includes", "content": finding['search_term']})
        action_step = {}
        if action_choice == '1': action_step = { "type": "close-connection" }
        elif action_choice == '2': action_step = { "type": "simple", "status": 403, "statusMessage": "Forbidden", "headers": {}, "data": "Blocked by generated privacy rule." }
        elif action_choice == '3': action_step = { "type": "passthrough", "uiType": "request-breakpoint" }
        elif action_choice == '4' and transform_map:
            original_value = finding['search_term']; new_value = transform_map.get(original_value, original_value)
            action_step = { "uiType": "req-res-transformer", "transformRequest": { "matchReplaceBody": [[{"source": original_value, "flags": "g"}, new_value]] }, "transformResponse": {} }
        rule = { "id": str(uuid.uuid4()), "type": "http", "activated": True, "matchers": matchers, "steps": [action_step], "completionChecker": { "type": "always" } }
        rules.append(rule)
    default_pass_through_rule = { "id": "default-wildcard", "type": "http", "activated": True, "matchers": [{"type": "wildcard", "uiType": "default-wildcard"}], "steps": [{"type": "passthrough"}], "completionChecker": {"type": "always"} }
    rules.append(default_pass_through_rule)
    final_json = { "id": "generated-privacy-rules", "title": "Generated Privacy Blocklist", "items": rules }
    try:
        with open(filename, 'w') as f: json.dump(final_json, f, indent=2)
        print(f"\n✅ Successfully generated rules file: '{filename}'")
        print("   Go to HTTP Toolkit -> Modify -> 'Import rules' to use it.")
    except Exception as e: print(f"\n❌ Error writing to file: {e}")

def interactive_session(findings):
    if not findings: print("[-] No occurrences matching your criteria were found."); return
    print(f"[+] Found {len(findings)} total matching occurrence(s).")
    while True:
        print("\n" + "---" * 15)
        for i, find in enumerate(findings):
            url_display = (find['url'][:75] + '...') if len(find['url']) > 75 else find['url']; print(f"  [{i+1}] {find['method']} to {find['hostname']} - Found '{BColors.HIGHLIGHT}{find['search_term']}{BColors.RESET}' in {find['location']}")
        print("---" * 15)
        try:
            choice = input(f"Enter a number to see details, 'g' to generate rules, or 'q' to quit: ")
            if choice.lower() == 'q': break
            elif choice.lower() == 'g':
                nums_to_export_str = input("Enter numbers to export (e.g., 1, 3, 4), or type 'all' for every finding: ")
                findings_to_export = []
                if nums_to_export_str.lower().strip() == 'all': findings_to_export = findings
                else:
                    try:
                        indices_to_export = [int(n.strip()) - 1 for n in nums_to_export_str.split(',')]; findings_to_export = [findings[i] for i in indices_to_export if 0 <= i < len(findings)]
                    except ValueError: print("Invalid input. Please enter numbers separated by commas or 'all'."); continue
                if not findings_to_export: print("No valid findings selected."); continue
                print(f"\nGenerating rules for {len(findings_to_export)} finding(s).")
                print("\nWhat kind of rule do you want to create?\n  [1] Close connection (Hard block)\n  [2] Return 403 Forbidden\n  [3] Pause for manual editing\n  [4] Automatically transform data")
                action_choice = input("Choose an action [1/2/3/4]: ")
                transform_map = None
                if action_choice == '4':
                    transform_map = {}; print("\nEnter the new values for each identifier:")
                    unique_terms_to_transform = sorted(list(set(f['search_term'] for f in findings_to_export)))
                    for term in unique_terms_to_transform:
                        new_value = input(f"  Replace '{term}' with: "); transform_map[term] = new_value
                elif action_choice not in ['1', '2', '3']: print("Invalid action choice."); continue
                filename = input("Enter a filename for the rules (default: httptoolkit-rules.json): ");
                if not filename: filename = "httptoolkit-rules.json"
                generate_rules_file(findings_to_export, action_choice, filename, transform_map)
            else:
                index = int(choice) - 1
                if 0 <= index < len(findings):
                    selected = findings[index]
                    print("\n" + "="*20 + f" Details for Finding #{index+1} " + "="*20)
                    print(f"Method:   {selected['method']}\nHost:     {selected['hostname']}\nFull URL: {selected['url']}")
                    print(f"Found:    '{BColors.HIGHLIGHT}{selected['search_term']}{BColors.RESET}'")
                    print(f"Location: {selected['location']}")
                    print("-" * 15 + " Context Snippet " + "-"*15); print(selected['context_snippet']); print("="*59)
                else: print("Invalid number. Please try again.")
        except (ValueError, IndexError): print("Invalid input. Please enter a number from the list, 'g', or 'q'.")
        except KeyboardInterrupt: print("\nExiting."); break

def summarize_hosts(har_file_path):
    """Counts and prints a sorted summary of all hosts contacted in a HAR file."""
    try:
        with open(har_file_path, 'r', encoding='utf-8') as f:
            har_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{har_file_path}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{har_file_path}'. Is it a valid HAR file?")
        return

    all_hosts = []
    for entry in har_data.get('log', {}).get('entries', []):
        url = entry.get('request', {}).get('url')
        if url:
            try:
                hostname = urlparse(url).hostname
                if hostname:
                    all_hosts.append(hostname)
            except Exception:
                continue
    
    if not all_hosts:
        print("No hosts found in the HAR file.")
        return

    host_counts = Counter(all_hosts)
    sorted_hosts = host_counts.most_common()
    output_lines = [f"{count} {host}" for host, count in sorted_hosts]
    print(", ".join(output_lines))

def main():
    parser = argparse.ArgumentParser(
        description="Interactively analyze a HAR file for specific data and generate HTTP Toolkit rules.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("har_file", help="Path to the .har file to analyze.")
    parser.add_argument(
        "--data", nargs='*', help="One-off specific data to search for (e.g., an email)."
    )
    parser.add_argument(
        '--device', help="Path to a text file containing device-specific IDs (one per line)."
    )
    parser.add_argument(
        "--method", nargs='+', help="Filter results for specific HTTP methods (e.g., POST GET)."
    )
    parser.add_argument(
        '--summarize-hosts', action='store_true',
        help="Print a count of all hosts contacted, sorted by frequency, then exit."
    )
    args = parser.parse_args()

    # If summarize flag is used, run that function and exit
    if args.summarize_hosts:
        summarize_hosts(args.har_file)
        return

    # The rest of the script runs only if --summarize-hosts is NOT used
    search_terms = []
    if args.device:
        try:
            with open(args.device, 'r') as f:
                for line in f:
                    clean_line = line.strip();
                    if clean_line: search_terms.append(clean_line)
        except FileNotFoundError:
            parser.error(f"The specified device ID file was not found: {args.device}")
    if args.data:
        search_terms.extend(args.data)
    if not search_terms:
        parser.error("No data to search for. You must use --data or --device (or --summarize-hosts).")
    
    final_search_terms = sorted(list(set(search_terms)))
    print(f"[*] Analyzing '{args.har_file}' for {len(final_search_terms)} specific term(s)...\n")
    
    all_findings = find_data_occurrences(args.har_file, final_search_terms, args.method)
    if all_findings is not None:
        interactive_session(all_findings)

if __name__ == "__main__":
    main()