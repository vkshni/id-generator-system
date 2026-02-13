import argparse
from engine import IDGenerator

def main():
    parser = argparse.ArgumentParser(
        description='ID Generator - Manage and generate unique IDs'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a new ID')
    generate_parser.add_argument('--type', required=True, help='ID type (order, user, etc.)')

    # Add ID type command
    add_parser = subparsers.add_parser('add', help='Add new ID type')
    add_parser.add_argument('--name', required=True, help='ID type name')
    add_parser.add_argument('--start', type=int, required=True, help='Start value')
    add_parser.add_argument('--step', type=int, required=True, help='Increment step')
    add_parser.add_argument('--prefix', required=True, help='Prefix (e.g., ORD-)')
    add_parser.add_argument('--padding', type=int, required=True, help='Number of digits')

    # Update ID type command
    update_parser = subparsers.add_parser('update', help='Update existing ID type')
    update_parser.add_argument('--name', required=True, help='ID type name')
    update_parser.add_argument('--start', type=int, help='Start value')
    update_parser.add_argument('--step', type=int, help='Increment step')
    update_parser.add_argument('--prefix', help='Prefix')
    update_parser.add_argument('--padding', type=int, help='Padding')

    # Delete ID type command
    delete_parser = subparsers.add_parser('delete', help='Delete ID type')
    delete_parser.add_argument('--name', required=True, help='ID type name')
    delete_parser.add_argument('--force', action='store_true', help='Force delete even if IDs exist')

    # Reset counter command
    reset_parser = subparsers.add_parser('reset', help='Reset counter to start value')
    reset_parser.add_argument('--name', required=True, help='ID type name')
    reset_parser.add_argument('--force', action='store_true', help='Force reset even if IDs exist')
    
    # We'll add commands here
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command is None:
        parser.print_help()
        return
    
    gen = IDGenerator()
    
    # Command handlers will go here

    if args.command == 'generate':
        try:
            id_val = gen.generate(args.type)
            print(f"✓ Generated: {id_val}")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif args.command == 'add':
        try:
            gen.add_id_type(args.name, args.start, args.step, args.prefix, args.padding)
            print(f"✓ ID type '{args.name}' added successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif args.command == 'update':
        try:
            kwargs = {}
            if args.start: kwargs['start_value'] = args.start
            if args.step: kwargs['increment_step'] = args.step
            if args.prefix: kwargs['prefix'] = args.prefix
            if args.padding: kwargs['padding'] = args.padding
            
            gen.update_id_type(args.name, **kwargs)
            print(f"✓ ID type '{args.name}' updated successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif args.command == 'delete':
        try:
            gen.delete_id_type(args.name, force=args.force)
            print(f"✓ ID type '{args.name}' deleted successfully")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif args.command == 'reset':
        try:
            gen.reset_counter(args.name, force=args.force)
            print(f"✓ Counter for '{args.name}' reset successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
    

if __name__ == '__main__':
    main()