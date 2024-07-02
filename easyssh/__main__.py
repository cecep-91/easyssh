import easyssh

if __name__ == "__main__":
    try:
        easyssh.main()
    except KeyboardInterrupt:
        quit()