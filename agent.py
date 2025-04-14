import click
from task_planner import TaskPlanner
from command_executor import CommandExecutor
from config import Config
import json

@click.command()
@click.argument('task_description')
def main(task_description):
    """AI Task Automation Agent"""
    click.echo(f"\n Task: {task_description}")
    
    # Step 1: Generate the plan
    planner = TaskPlanner()
    try:
        plan = planner.generate_plan(task_description)
    except Exception as e:
        click.echo(f" Failed to create plan: {e}")
        return
    
    # Display the plan
    click.echo("\n Plan:")
    click.echo(f"Description: {plan.get('description', 'No description')}")
    
    if 'commands' in plan:
        click.echo("\n Commands to execute:")
        for cmd in plan['commands']:
            click.echo(f" - {cmd}")
    
    if 'files' in plan:
        click.echo("\n Files to create/modify:")
        for file in plan['files']:
            click.echo(f" - {file.get('path', 'unknown')}")
    
    if 'warnings' in plan:
        click.echo(f"\n Warnings: {plan['warnings']}")
    
    # Get user approval
    if Config.SAFE_MODE and not click.confirm("\n👉 Do you want to proceed with this plan?"):
        click.echo(" Task cancelled by user.")
        
        # Ask why the user rejected the plan
        reason = click.prompt("Please provide the reason for rejecting the plan", type=str)
        click.echo(f"User feedback: {reason}")
        
        # Refine the task description based on the user's feedback
        refined_task = f"Original task: {task_description}. Error occurred: {reason}. Please fix the plan."
        
        # Regenerate the plan using the refined task description
        try:
            refined_plan = planner.generate_plan(refined_task)
            click.echo("\n Refined Plan:")
            click.echo(f"Description: {refined_plan.get('description', 'No description')}")
            
            if 'commands' in refined_plan:
                click.echo("\n Commands to execute:")
                for cmd in refined_plan['commands']:
                    click.echo(f" - {cmd}")
            
            if 'files' in refined_plan:
                click.echo("\n Files to create/modify:")
                for file in refined_plan['files']:
                    click.echo(f" - {file.get('path', 'unknown')}")
            
            if 'warnings' in refined_plan:
                click.echo(f"\n Warnings: {refined_plan['warnings']}")
            
            # Ask for user approval again on the refined plan
            if Config.SAFE_MODE and click.confirm("\n👉 Do you want to proceed with the refined plan?"):
                # Execute the refined plan
                executor = CommandExecutor()
                if 'commands' in refined_plan:
                    success, message = executor.execute_commands(refined_plan['commands'])
                    if not success:
                        click.echo(f"\nTask failed: {message}")
                        return
                
                # Handle file operations for the refined plan
                if 'files' in refined_plan:
                    for file in refined_plan['files']:
                        try:
                            with open(file['path'], 'w') as f:
                                f.write(file.get('content', ''))
                            click.echo(f"Created/updated file: {file['path']}")
                        except Exception as e:
                            click.echo(f"Failed to create file {file['path']}: {e}")
                            return
                
                click.echo("\nTask completed successfully!")
        except Exception as e:
            click.echo(f"Failed to refine plan: {e}")
        return
    
    # If the original plan was accepted, execute it
    executor = CommandExecutor()
    if 'commands' in plan:
        success, message = executor.execute_commands(plan['commands'])
        if not success:
            click.echo(f"\nTask failed: {message}")
            return
    
    # Handle file operations
    if 'files' in plan:
        for file in plan['files']:
            try:
                with open(file['path'], 'w') as f:
                    f.write(file.get('content', ''))
                click.echo(f"Created/updated file: {file['path']}")
            except Exception as e:
                click.echo(f"Failed to create file {file['path']}: {e}")
                return
    
    task_success=click.confirm("\nTask completed. Was the task successful? (yes/no): ")
    if task_success:
        click.echo("\nTask completed successfully!")
    else:
        click.echo("\nTask failed. Please provide the reason for failure.")
        failure_reason = click.prompt("Reason for failure:", type=str)
        click.echo(f"User feedback: {failure_reason}")
        refined_task = f"Original task: {task_description}. Error occurred: {failure_reason}. Please fix the plan."
        
        try:
            refined_plan = planner.generate_plan(refined_task)
            click.echo("\n Refined Plan:")
            click.echo(f"Description: {refined_plan.get('description', 'No description')}")
            
            if 'commands' in refined_plan:
                click.echo("\n Commands to execute:")
                for cmd in refined_plan['commands']:
                    click.echo(f" - {cmd}")
            
            if 'files' in refined_plan:
                click.echo("\n Files to create/modify:")
                for file in refined_plan['files']:
                    click.echo(f" - {file.get('path', 'unknown')}")
            
            if 'warnings' in refined_plan:
                click.echo(f"\n Warnings: {refined_plan['warnings']}")
            
            # Ask for user approval again on the refined plan
            if Config.SAFE_MODE and click.confirm("\n👉 Do you want to proceed with the refined plan?"):
                # Execute the refined plan
                executor = CommandExecutor()
                if 'commands' in refined_plan:
                    success, message = executor.execute_commands(refined_plan['commands'])
                    if not success:
                        click.echo(f"\nTask failed: {message}")
                        return
                
                # Handle file operations for the refined plan
                if 'files' in refined_plan:
                    for file in refined_plan['files']:
                        try:
                            with open(file['path'], 'w') as f:
                                f.write(file.get('content', ''))
                            click.echo(f"Created/updated file: {file['path']}")
                        except Exception as e:
                            click.echo(f"Failed to create file {file['path']}: {e}")
                            return
                
                click.echo("\nTask completed successfully!")
        except Exception as e:
            click.echo(f"Failed to refine plan: {e}")
        return

if __name__ == "__main__":
    main()
