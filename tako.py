import requests
import json
import os
from typing import Dict, Optional, List, Any
from dotenv import load_dotenv

load_dotenv()


class TakoAPI:

    BASE_URL = "https://open-api.tako.so/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json", "x-api-key": api_key}

    def create_cast(
        self,
        text: Optional[str] = None,
        title: Optional[str] = None,
        community_id: Optional[str] = None,
        mentions: Optional[List[int]] = None,
        mentions_positions: Optional[List[int]] = None,
        urls: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new cast (post) on Tako."""
        if not text and not title:
            raise ValueError("Either text or title must be provided")

        data = {
            "text": text or "",
            "title": title or "",
            "community_id": community_id or "",
            "mentions": mentions or [],
            "mentions_positions": mentions_positions or [],
            "urls": urls or [],
        }

        response = requests.post(
            f"{self.BASE_URL}/cast", headers=self.headers, json=data
        )
        response.raise_for_status()
        return response.json()

    def reply_to_cast(
        self,
        cast_hash: str,
        text: str,
        mentions: Optional[List[int]] = None,
        mentions_positions: Optional[List[int]] = None,
        urls: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Reply to an existing cast."""
        data = {
            "cast_hash": cast_hash,
            "text": text,
            "mentions": mentions,
            "mentions_positions": mentions_positions,
            "urls": urls,
        }

        response = requests.post(
            f"{self.BASE_URL}/cast/reply", headers=self.headers, json=data
        )
        response.raise_for_status()
        return response.json()

    def get_feed_by_fids(
        self, fids: List[int], cursor: Optional[int] = None
    ) -> Dict[str, Any]:
        """Fetch feed based on a list of FIDs."""
        params = {"target_type": "fid", "target_ids": ",".join(map(str, fids))}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            f"{self.BASE_URL}/feed/cast", headers=self.headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def get_feed_by_communities(
        self, community_ids: List[str], cursor: Optional[int] = None
    ) -> Dict[str, Any]:
        """Fetch feed based on a list of community IDs."""
        params = {"target_type": "community", "target_ids": ",".join(community_ids)}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            f"{self.BASE_URL}/feed/cast", headers=self.headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def get_following_feed(self) -> Dict[str, Any]:
        """Fetch feed based on following users."""
        response = requests.get(f"{self.BASE_URL}/feed/follow", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_image_upload_url(self) -> str:
        """Get URL for uploading images."""
        response = requests.post(
            f"{self.BASE_URL}/image_upload_url", headers=self.headers
        )
        response.raise_for_status()
        return response.json()["data"]["url"]


def get_tako_recommendations(
    cursor: str = "eyJzZXNzaW9uX2lkIjoiMDFKTTNHTTcxTjZOSlhQWVFWMzE4RVBITTAiLCJjdXJzb3IiOiIyMCIsInBhZ2UiOjJ9",
    limit: int = 10,
    auth_token: str = "0xc62fcbd0920d9ed49f5fc71290e9bdf1f2d2e04ecd8d4a0d57d297f670bd10cf451e81f902a8e641d1128865f7aaef95fd673b96300685f280bf650608fc3f061b:1739666249",
) -> Dict:
    url = "https://api.tako.so/v1/feed/community/recommend"

    # Query parameters
    params = {"cursor": cursor, "limit": limit}

    # Headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Origin": "https://app.tako.so",
        "Referer": "https://app.tako.so/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-hotfixversion": "1737442813",
        "x-lang": "zh-CN",
        "x-platform": "web",
        "x-request-auth": auth_token,
    }

    # Send GET request
    response = requests.get(url, params=params, headers=headers)

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "data": response.json() if response.status_code == 200 else None,
    }


def format_response(response_data: Dict) -> None:
    print(f"\nStatus Code: {response_data['status_code']}")

    print("\nResponse Headers:")
    for key, value in response_data["headers"].items():
        print(f"{key:40}: {value}")

    if response_data["data"]:
        print("\nResponse Data:")
        print(json.dumps(response_data["data"], indent=2, ensure_ascii=False))


def test_create_cast():
    """Test creating a new cast."""
    api_key = os.getenv("TAKO_API_KEY")
    tako = TakoAPI(api_key)

    try:
        # Test with text only
        result = tako.create_cast(text="Test cast from API")
        print("✓ Create cast with text only:", result)

        # Test with all parameters matching curl format
        # result = tako.create_cast(
        #     text="content testing",
        #     title="",
        #     community_id="",
        #     mentions=[],
        #     mentions_positions=[],
        #     urls=[],
        # )
        # print("✓ Create cast with all params:", result)

        # # Test error case - no text or title
        # try:
        #     tako.create_cast()
        #     print("✗ Create cast without text/title should fail")
        # except ValueError:
        #     print("✓ Create cast without text/title failed as expected")

    except Exception as e:
        print(f"✗ Create cast test failed: {str(e)}")


def test_reply_to_cast():
    api_key = os.getenv("TAKO_API_KEY")
    tako = TakoAPI(api_key)

    try:
        result = tako.reply_to_cast(
            cast_hash="0x15c5b3244d4bad773299037a0030a126d00cdd20", text="Test reply"
        )
        print("✓ Basic reply:", result)

        result = tako.reply_to_cast(
            cast_hash="0x15c5b3244d4bad773299037a0030a126d00cdd20",
            text="Test reply with @mention",
            mentions=[],
            mentions_positions=[],
            urls=["https://example.com/image.jpg"],
        )
        print("✓ Reply with mentions and URLs:", result)

    except Exception as e:
        print(f"✗ Reply test failed: {str(e)}")


def test_get_feeds():
    api_key = os.getenv("TAKO_API_KEY")
    tako = TakoAPI(api_key)

    try:
        # result = tako.get_feed_by_fids([13475, 10636])
        # print("✓ Get feed by FIDs:", result)

        # result = tako.get_feed_by_communities(["tako", "farcaster"])
        # print("✓ Get feed by communities:", result)

        result = tako.get_following_feed()
        print("✓ Get following feed:", result)

    except Exception as e:
        print(f"✗ Feed test failed: {str(e)}")


def test_get_recommendations():
    """Test getting Tako recommendations."""
    try:
        result = get_tako_recommendations()
        print("✓ Get recommendations:", result["status_code"])
        if result["status_code"] == 200:
            print("✓ Recommendations data retrieved successfully")
        else:
            print(f"✗ Failed to get recommendations: {result['status_code']}")
    except Exception as e:
        print(f"✗ Recommendations test failed: {str(e)}")


def test_image_upload():
    """Test getting image upload URL."""
    api_key = os.getenv("TAKO_API_KEY")
    tako = TakoAPI(api_key)

    try:
        result = tako.get_image_upload_url()
        print("✓ Get image upload URL:", result)

    except Exception as e:
        print(f"✗ Image upload URL test failed: {str(e)}")


def run_all_tests():
    """Run all Tako API tests."""
    print("\n=== Running Tako API Tests ===\n")

    # print("Testing Recommendations:")
    # test_get_recommendations()

    if os.getenv("TAKO_API_KEY"):
        # print("\nTesting Create Cast:")
        # test_create_cast()

        # print("\nTesting Reply to Cast:")
        # test_reply_to_cast()

        print("\nTesting Feed Retrieval:")
        test_get_feeds()

        # print("\nTesting Image Upload:")
        # test_image_upload()
    else:
        print("\nSkipping API tests - TAKO_API_KEY not set")

    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    run_all_tests()
