# Organize 📂

Got a super messy folder? This project automatically organize your unstructured files into logical folders based on their names and types. 

Instead of manually sorting through hundreds of downloads or project files, this script reads your folder's contents, asks the LLM to figure out a smart directory structure, and then moves everything into its right place.

## Working

1. **Scan:** The script recursively reads all file names(no file data is touched) inside the target folder (`FolderToOrganize`), ignoring hidden/system files.
2. **Plan:** It sends the list of relative file paths to an AI model with a strict prompt to categorize them based on file types and names (e.g., moving `notes.txt` to a `Documents` folder).
3. **Execute:** The agent returns a JSON dictionary of the plan. Python parses this, auto-creates any missing directories, and safely moves the files to their new locations.

## Setup
1. Clone the repository
```
git clone https://github.com/theprajwaldongare/Organize.git
cd Organize
```
2. Install dependencies(venv): ```pip install openai python-dotenv```

3. Add your API key

    ```
    # Create a .env file in the project directory:
    API_KEY=your_api_key
    ```
4. Give the Folder URL
    ```
    # replace FolderToOrganize with the Folder URL
    folderUrl = "FolderToOrganize"
    ```


5. Run the agent
```python agent.py```

The agent will scan the folder, generate an organization plan, ask for your permission to proceed, and then create the required folders and move the files.

## Technical Details
The script uses the standard openai Python SDK, but modifies the base URL to connect to Google's Generative AI endpoint. It passes your current folder structure to the AI with a strict prompt to return a JSON map. The JSON maps the original file paths to the new destination paths,then the Python script safely move the files using standard os commands.