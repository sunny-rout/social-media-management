# SocialMediaManagementAutomation Crew

Welcome to the SocialMediaManagementAutomation Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```
Run the following command to install crewai CLI:

```bash
uv tool install crewai
```
If you encounter a PATH warning, run this command to update your shell:

```bash
uv tool update-shell
```

To verify that crewai is installed, run:

```bash
uv tool list
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/social_media_management_automation/config/agents.yaml` to define your agents
- Modify `src/social_media_management_automation/config/tasks.yaml` to define your tasks
- Modify `src/social_media_management_automation/crew.py` to add your own logic, tools and specific args
- Modify `src/social_media_management_automation/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the social_media_management_automation Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The social_media_management_automation Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the SocialMediaManagementAutomation Crew or crewAI.
- Visit [documentation](https://docs.crewai.com)
- Reach out [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with docs](https://chatg.pt/DWjSBZn)
