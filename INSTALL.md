# Install KBs

The KBs plugin helps ChatGPT and Codex connect to your knowledge bases. Install
it first, then use its setup guide to connect your account.

## Install from your organisation's directory

1. Open the ChatGPT or Codex desktop app and sign into the account your
   organisation uses for KB access.
2. Open **Settings → Plugins** and select the **Plugins** tab.
3. If **KBs** is already in the list, check that its switch is on (blue).
   You can then go straight to **Start setup** below.
4. Otherwise, click **Browse directory**.
5. Select the tab bearing your organisation's name.
6. Search for **KBs**, then open the result described as
   **Use and manage multiple independent KB services**.
7. Click the **Install** button or the **+** installation button on its details
   page. Follow any prompts to connect the included MCP Service.
8. Return to **Settings → Plugins → Plugins**, find **KBs**, and check that its
   switch is on (blue). Click the switch if it is off (grey).

If KBs is not listed in your organisation's directory, ask the person who manages
your KB access to make it available. Installing it does not itself give you
access to someone else's knowledge base.

## Start setup

Start a **new chat** in the application where you want to use the KBs and say:

> Set up my knowledge bases. Guide me through the connections and sign-in steps
> I need to complete, then check that access works.

The plugin supplies the setup instructions for that application. Local Codex's
native MCP connections are configured in its desktop settings; registered cloud
connections for ChatGPT are configured at **chatgpt.com in a browser**. Installing
the plugin does not make those two connection routes interchangeable.

For local Codex, you can also read the
[step-by-step connection guide](setup/openai-client-setup.md) here. Repeat setup
on each computer where you use Codex.

## For the person providing the plugin

Publish/import KBs into the intended workspace directory and make it available
to the intended users before sending them these instructions. The public
directory need not list this workspace plugin. Keep the published package and
its setup guide aligned. Source changes in this repository do not update an
already installed plugin; use the client's supported plugin update mechanism.
