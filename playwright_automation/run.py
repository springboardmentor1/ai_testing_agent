from generated_script import run_form_test, run_google_test

print("Choose Test Type")
print("1. Form Test (Manual UI Input)")
print("2. Google Test (Full Automation)")

choice = input("Enter option (1 or 2): ")

if choice == "1":
    run_form_test()
elif choice == "2":
    run_google_test()
else:
    print("Invalid option")
