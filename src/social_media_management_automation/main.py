#!/usr/bin/env python
import sys
import argparse
from social_media_management_automation.crew import SocialMediaManagementAutomationCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(args):
    """
    Run the crew.
    """
    inputs = {
        'company_name': args.company_name,
        'target_platforms': args.target_platforms,
        'industry': args.industry
    }
    SocialMediaManagementAutomationCrew().crew().kickoff(inputs=inputs)


def train(args):
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company_name': args.company_name,
        'target_platforms': args.target_platforms,
        'industry': args.industry
    }
    try:
        SocialMediaManagementAutomationCrew().crew().train(n_iterations=args.n_iterations, filename=args.filename, inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay(args):
    """
    Replay the crew execution from a specific task.
    """
    try:
        SocialMediaManagementAutomationCrew().crew().replay(task_id=args.task_id)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test(args):
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'company_name': args.company_name,
        'target_platforms': args.target_platforms,
        'industry': args.industry
    }
    try:
        SocialMediaManagementAutomationCrew().crew().test(n_iterations=args.n_iterations, openai_model_name=args.openai_model_name, inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Social Media Management Automation crew.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Common arguments for crew inputs
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument('--company-name', type=str, default='AI Startup', help='Name of the company.')
    input_parser.add_argument('--target-platforms', type=str, default='LinkedIn, Twitter', help='Target social media platforms.')
    input_parser.add_argument('--industry', type=str, default='Artificial Intelligence', help='Industry of the company.')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run the crew.', parents=[input_parser])
    run_parser.set_defaults(func=run)

    # Train command
    train_parser = subparsers.add_parser('train', help='Train the crew.', parents=[input_parser])
    train_parser.add_argument('n_iterations', type=int, help='Number of iterations for training.')
    train_parser.add_argument('filename', type=str, help='Filename to save training data.')
    train_parser.set_defaults(func=train)

    # Replay command
    replay_parser = subparsers.add_parser('replay', help='Replay a task.')
    replay_parser.add_argument('task_id', type=str, help='Task ID to replay.')
    replay_parser.set_defaults(func=replay)

    # Test command
    test_parser = subparsers.add_parser('test', help='Test the crew.', parents=[input_parser])
    test_parser.add_argument('n_iterations', type=int, help='Number of iterations for testing.')
    test_parser.add_argument('openai_model_name', type=str, help='OpenAI model name to use for testing.')
    test_parser.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)
