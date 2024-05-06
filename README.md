## Instructions
To run the code present in this repository, follow these steps:

1. Clone the code from the "main" branch to your local machine.
2. In your terminal, navigate to the directory where the repository code was downloaded.
3. Execute the command "docker build -t romba-unit-app ."
4. Execute the command "docker run -v $(pwd):/app romba-unit-app"

After executing the commands above, a folder named "schema" will be created containing the entity files.
