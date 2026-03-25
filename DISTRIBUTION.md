# Distribution and Updates

Because **GATE** is designed to be an extensible, constantly updated research tool, there are two separate workflows for lab members depending on their technical expertise.

## 1. Developers (Adding Tools & Code)
Lab members who want to actively write new computational chemistry tools or modify the dashboard **must run the application from the source code**.

**Workflow for Developers:**
1. Clone the repository: `git clone https://github.com/DesireBonneau/ui-program`
2. Set up the Conda environment (see `README.md`).
3. Add their new scripts to `src/tools/` and register them in `src/main.py`.
4. Commit and push their changes: `git pull`, `git add .`, `git commit -m "Added Tool X"`, `git push origin main`.

*For Developers, updating the app is instantaneous—they simply run `git pull` in their terminal to pull down their colleagues' newest tools.*

---

## 2. End-Users (Running Calculations Only)
Lab members who do not code and simply want to execute the chemistry algorithms should use the compiled standalone `GATE.exe` file.

The `.exe` is a frozen snapshot of the code. **It cannot automatically download new tools from GitHub.**

**Workflow for End-Users:**
1. Go to the repository's [Releases](https://github.com/DesireBonneau/ui-program/releases) page.
2. Download the latest `GATE.zip` release.
3. Extract the folder to your Desktop.
4. Double-click `GATE.exe` to launch the application.

*When Developers announce a new version of the app, End-Users must manually delete their old `GATE` folder and download the newly published `.zip` from GitHub.*

---

## How to Compile a New Release (For Administrators)
When Developers have merged several new tools into the repository and you want to publish an update for the End-Users, you must bundle a new `.exe`.

1. Open your terminal and activate your Conda environment:
   ```bash
   conda activate ui-program
   ```
2. Make sure your local code is fully updated:
   ```bash
   git pull origin main
   ```
3. Run the PyInstaller build command from the root directory:
   ```powershell
   pyinstaller --noconsole --name "GATE" `
     --add-data "src/tkinter_theme;tkinter_theme" `
     --add-data "src/data;data" `
     --add-data "src/tools;tools" `
     --hidden-import "rdkit" `
     --hidden-import "pandas" `
     --hidden-import "matplotlib" `
     --hidden-import "numpy" `
     --hidden-import "tqdm" `
     src/main.py
   ```
4. Once completed, navigate to the `dist/` directory, right-click the `GATE` folder, and **Compress to ZIP file**.
5. Go to the GitHub repository, click **Draft a new release**, attach the `GATE.zip` file, and publish!
