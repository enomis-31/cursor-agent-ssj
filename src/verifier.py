import json
from openai import OpenAI
from src.utils import get_env_var, logger

# ... existing code ...

def run_verification(task_id, spec_content, agent_output_summary):
    """
    Orchestrate verification for a specific task.
    """
    # In a real scenario, we might extract specific user stories/criteria from spec_content
    # For now, we pass the relevant context to GPT-mini.
    return verify_task_completion(f"Task {task_id}", spec_content, agent_output_summary)
    """
    Use GPT-mini to verify if the Cloud Agent output satisfies the requirements.
    Returns: (status, feedback) where status is 'pass' or 'fail'.
    """
    client = OpenAI(api_key=get_env_var("OPENAI_API_KEY"))
    
    prompt = f"""
    Verify if the following task has been successfully completed.
    
    ### Task Description:
    {task_description}
    
    ### Acceptance Criteria:
    {acceptance_criteria}
    
    ### Agent Output Summary:
    {agent_output_summary}
    
    Determine if ALL acceptance criteria are satisfied.
    Return a JSON response with:
    - "status": "pass" or "fail"
    - "feedback": A brief explanation of what was satisfied and what is missing (differential feedback).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise quality assurance assistant for a coding orchestrator."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        result = response.choices[0].message.content
        import json
        data = json.loads(result)
        
        status = data.get("status", "fail")
        feedback = data.get("feedback", "No feedback provided.")
        
        logger.info(f"Verification finished with status: {status}")
        return status, feedback
        
    except Exception as e:
        logger.error(f"Verification failed with error: {e}")
        return "fail", f"Verification system error: {str(e)}"
