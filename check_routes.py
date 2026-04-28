import app

print("Checking Flask routes...")
print("\nAll registered routes:")
for rule in app.app.url_map.iter_rules():
    print(f"  Endpoint: {rule.endpoint:30} -> {rule.rule}")

print("\n\nLooking for 'collections' routes:")
for rule in app.app.url_map.iter_rules():
    if 'collection' in rule.endpoint or 'collection' in rule.rule:
        print(f"  ✓ {rule.endpoint:30} -> {rule.rule}")
