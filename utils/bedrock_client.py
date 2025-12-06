import boto3
import json
from typing import Dict, Any

class BedrockClient:
    """Simple client for AWS Bedrock Claude models"""

    def __init__(self, region_name: str = "us-east-1"):
        """
        Initialize Bedrock client

        Args:
            region_name: AWS region where Bedrock is available
        """
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        # Use cross-region inference profile instead of direct model ID
        self.model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

    def generate_player_comparison(
        self,
        player1_name: str,
        player2_name: str,
        season1: str,
        season2: str,
        player1_stats: Dict[str, Any],
        player2_stats: Dict[str, Any]
    ) -> str:
        """
        Generate AI-powered comparison insights between two NBA players

        Args:
            player1_name: Name of first player
            player2_name: Name of second player
            season1: Season for first player
            season2: Season for second player
            player1_stats: Stats dictionary for first player
            player2_stats: Stats dictionary for second player

        Returns:
            AI-generated comparison text
        """

        # Prepare stats for the prompt
        stats_comparison = f"""
Player 1: {player1_name} ({season1})
- PPG: {player1_stats['PTS']:.1f}
- RPG: {player1_stats['REB']:.1f}
- APG: {player1_stats['AST']:.1f}
- FG%: {player1_stats['FG_PCT']:.3f}
- 3P%: {player1_stats['FG3_PCT']:.3f}
- FT%: {player1_stats['FT_PCT']:.3f}
- SPG: {player1_stats['STL']:.1f}
- BPG: {player1_stats['BLK']:.1f}

Player 2: {player2_name} ({season2})
- PPG: {player2_stats['PTS']:.1f}
- RPG: {player2_stats['REB']:.1f}
- APG: {player2_stats['AST']:.1f}
- FG%: {player2_stats['FG_PCT']:.3f}
- 3P%: {player2_stats['FG3_PCT']:.3f}
- FT%: {player2_stats['FT_PCT']:.3f}
- SPG: {player2_stats['STL']:.1f}
- BPG: {player2_stats['BLK']:.1f}
"""

        prompt = f"""You are an NBA analyst comparing two players' seasons. Based on these statistics, provide a concise, insightful comparison (3-4 paragraphs max):

{stats_comparison}

Focus on:
1. Overall performance and scoring efficiency
2. Playmaking and defensive contributions
3. Key strengths and weaknesses for each player
4. Which player had the better season and why

Be specific with numbers but write in an engaging, analytical style."""

        # Prepare request body for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        try:
            # Invoke the model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']

        except Exception as e:
            return f"Error generating AI insights: {str(e)}\n\nPlease ensure:\n1. AWS credentials are configured\n2. Bedrock model access is enabled in AWS Console\n3. IAM permissions are set up correctly"
