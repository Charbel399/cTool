import extract_uncertainty_tasks

def main():
    tasks_names = extract_uncertainty_tasks.extract_uncertainty_tasks("C:\\Users\\ashle\\OneDrive\\Desktop\\TorrentTO.xmi")

    # Print the results
    print("The Tasks Creating Uncertainty Are:")
    for name in tasks_names:
             print("- " + name)

if __name__ == "__main__":
    main()