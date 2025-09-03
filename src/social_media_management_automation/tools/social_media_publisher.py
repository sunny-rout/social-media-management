from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any, List
import json
import random
from datetime import datetime, timedelta

class SocialMediaPostRequest(BaseModel):
    """Input schema for Social Media Publisher Tool."""
    platform: str = Field(..., description="Target social media platform (Twitter, LinkedIn, Facebook, Instagram)")
    content: str = Field(..., description="The content to be posted")
    image_url: Optional[str] = Field(None, description="Optional URL of image to attach to the post")
    scheduled_time: Optional[str] = Field(None, description="Optional scheduled time in ISO format (YYYY-MM-DD HH:MM:SS)")

class SocialMediaPublisherTool(BaseTool):
    """Tool for simulating social media posts across multiple platforms with platform-specific optimizations."""

    name: str = "social_media_publisher"
    description: str = (
        "Simulates posting content to social media platforms (Twitter, LinkedIn, Facebook, Instagram) "
        "with platform-specific formatting, character limits, and optimization rules. "
        "Returns structured response with simulated post details including post ID, formatted content, "
        "and estimated reach metrics."
    )
    args_schema: Type[BaseModel] = SocialMediaPostRequest

    def _run(self, platform: str, content: str, image_url: Optional[str] = None, scheduled_time: Optional[str] = None) -> str:
        try:
            # Validate platform
            supported_platforms = ["Twitter", "LinkedIn", "Facebook", "Instagram"]
            platform_normalized = platform.capitalize()
            
            if platform_normalized not in supported_platforms:
                return json.dumps({
                    "error": f"Platform '{platform}' is not supported. Supported platforms: {', '.join(supported_platforms)}",
                    "supported_platforms": supported_platforms
                })

            # Generate simulated post ID
            post_id = f"{platform_normalized.lower()}_{random.randint(100000, 999999)}"

            # Apply platform-specific formatting
            formatted_content = self._format_content_for_platform(platform_normalized, content)
            
            # Handle scheduling
            if scheduled_time:
                try:
                    scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
                    status = "scheduled"
                except ValueError:
                    return json.dumps({
                        "error": "Invalid scheduled_time format. Please use ISO format: YYYY-MM-DD HH:MM:SS"
                    })
            else:
                scheduled_dt = datetime.now()
                status = "published"

            # Generate platform-specific estimated reach
            estimated_reach = self._calculate_estimated_reach(platform_normalized, len(content), bool(image_url))

            # Prepare response
            response = {
                "post_id": post_id,
                "platform": platform_normalized,
                "formatted_content": formatted_content,
                "original_content": content,
                "image_url": image_url,
                "scheduled_time": scheduled_dt.isoformat(),
                "status": status,
                "estimated_reach": estimated_reach,
                "platform_insights": self._get_platform_insights(platform_normalized, content, image_url),
                "formatting_applied": self._get_formatting_details(platform_normalized, content)
            }

            return json.dumps(response, indent=2)

        except Exception as e:
            return json.dumps({"error": f"An error occurred while processing the post: {str(e)}"})

    def _format_content_for_platform(self, platform: str, content: str) -> str:
        """Apply platform-specific formatting rules."""
        
        if platform == "Twitter":
            # Twitter: 280 character limit
            if len(content) > 280:
                formatted = content[:277] + "..."
            else:
                formatted = content
            
            # Add hashtag recommendations if none exist
            if "#" not in content:
                formatted += " #SocialMedia"
                
            return formatted

        elif platform == "LinkedIn":
            # LinkedIn: Professional tone, longer content allowed
            formatted = content
            
            # Add professional call-to-action if short post
            if len(content) < 100:
                formatted += "\n\nWhat are your thoughts on this? Share your experience in the comments!"
                
            return formatted

        elif platform == "Facebook":
            # Facebook: Engagement-focused formatting
            formatted = content
            
            # Add engagement elements
            if "?" not in content:
                formatted += "\n\nWhat do you think? Let us know in the comments!"
                
            return formatted

        elif platform == "Instagram":
            # Instagram: Visual-first approach, hashtag optimization
            formatted = content
            
            # Add relevant hashtags if missing
            if "#" not in content:
                hashtags = ["#instagram", "#content", "#social", "#engagement", "#community"]
                formatted += "\n\n" + " ".join(hashtags[:3])
                
            return formatted

        return content

    def _calculate_estimated_reach(self, platform: str, content_length: int, has_image: bool) -> Dict[str, Any]:
        """Calculate simulated estimated reach based on platform and content characteristics."""
        
        base_reach = {
            "Twitter": random.randint(50, 500),
            "LinkedIn": random.randint(100, 1000),
            "Facebook": random.randint(200, 1500),
            "Instagram": random.randint(300, 2000)
        }

        reach = base_reach.get(platform, 100)
        
        # Boost for images
        if has_image:
            reach = int(reach * 1.5)
            
        # Optimal content length boost
        if platform == "Twitter" and 100 <= content_length <= 280:
            reach = int(reach * 1.2)
        elif platform == "LinkedIn" and 150 <= content_length <= 300:
            reach = int(reach * 1.3)
        elif platform in ["Facebook", "Instagram"] and content_length >= 100:
            reach = int(reach * 1.2)

        return {
            "estimated_impressions": reach,
            "estimated_engagements": int(reach * 0.05),
            "estimated_clicks": int(reach * 0.02),
            "confidence_score": round(random.uniform(0.7, 0.95), 2)
        }

    def _get_platform_insights(self, platform: str, content: str, image_url: Optional[str]) -> Dict[str, Any]:
        """Generate platform-specific insights and recommendations."""
        
        insights = {
            "Twitter": {
                "character_count": len(content),
                "character_limit": 280,
                "optimal_hashtags": "1-2",
                "best_posting_time": "9 AM - 10 AM, 7 PM - 9 PM",
                "recommendation": "Keep it concise and engaging. Add relevant hashtags."
            },
            "LinkedIn": {
                "character_count": len(content),
                "optimal_length": "150-300 characters for high engagement",
                "best_posting_time": "Tuesday - Thursday, 8 AM - 10 AM",
                "recommendation": "Professional tone works best. Ask questions to drive engagement."
            },
            "Facebook": {
                "character_count": len(content),
                "optimal_length": "40-80 characters for highest engagement",
                "best_posting_time": "1 PM - 4 PM, 6 PM - 9 PM",
                "recommendation": "Visual content performs 2.3x better. Ask questions to boost engagement."
            },
            "Instagram": {
                "character_count": len(content),
                "caption_limit": 2200,
                "optimal_hashtags": "5-10",
                "best_posting_time": "6 AM - 9 AM, 7 PM - 8 PM",
                "recommendation": "High-quality visuals are essential. Use relevant hashtags strategically."
            }
        }

        platform_insight = insights.get(platform, {})
        
        # Add image analysis
        if image_url:
            platform_insight["image_attached"] = True
            platform_insight["performance_boost"] = "+50% estimated reach"
        else:
            platform_insight["image_attached"] = False
            platform_insight["suggestion"] = "Consider adding an image to increase engagement"

        return platform_insight

    def _get_formatting_details(self, platform: str, original_content: str) -> Dict[str, Any]:
        """Return details about what formatting was applied."""
        
        details = {
            "platform": platform,
            "original_length": len(original_content),
            "modifications": []
        }

        if platform == "Twitter" and len(original_content) > 280:
            details["modifications"].append("Content truncated to fit 280 character limit")
            
        if platform == "Twitter" and "#" not in original_content:
            details["modifications"].append("Added hashtag for better discoverability")
            
        if platform == "LinkedIn" and len(original_content) < 100:
            details["modifications"].append("Added professional call-to-action")
            
        if platform == "Facebook" and "?" not in original_content:
            details["modifications"].append("Added engagement question")
            
        if platform == "Instagram" and "#" not in original_content:
            details["modifications"].append("Added relevant hashtags for better reach")

        if not details["modifications"]:
            details["modifications"].append("No modifications needed - content optimized for platform")

        return details