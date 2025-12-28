
from engine import DatabaseEngine


def print_banner():
    print("=" * 50)
    print("Mini Database Engine v1.0")
    print("Type 'EXIT' or 'QUIT' to exit")
    print("=" * 50)


def main():
    print_banner()
    engine = DatabaseEngine()
    
    while True:
        try:
            command = input("\ndb> ").strip()
            
            if not command:
                continue
                
            if command.upper() in ('EXIT', 'QUIT'):
                print("Goodbye!")
                break
            
            result = engine.execute(command)
            
            if result is not None:
                print(result)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
