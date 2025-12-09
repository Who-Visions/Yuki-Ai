from yuki_local import YukiLocal
import time

def test_yuki_v06():
    print("🦊 Initializing Yuki v0.06-local...")
    yuki = YukiLocal()
    
    # Test 1: Image Generation with specific parameters
    print("\n[TEST 1] Image Generation (16:9, 4K)")
    query_image = "Generate a cinematic cosplay photo of a cyberpunk samurai in Neon Tokyo. I want it in 16:9 aspect ratio and 4K resolution."
    response_image = yuki.query(query_image)
    print(f"Response: {response_image['output']}")
    print(f"Model Used: {response_image['model']}")
    
    # Test 2: Complex Research (Gemini 3 routing)
    print("\n[TEST 2] Complex Research (Gemini 3)")
    query_research = "Research the history of samurai armor materials and how they could be adapted for modern cosplay using EVA foam. Create a detailed plan."
    response_research = yuki.query(query_research)
    print(f"Response: {response_research['output'][:200]}...")
    print(f"Model Used: {response_research['model']}")

    # Test 3: Video Generation
    print("\n[TEST 3] Video Generation")
    query_video = "Create a video of the cyberpunk samurai drawing their katana in slow motion. 16:9 aspect ratio."
    response_video = yuki.query(query_video)
    print(f"Response: {response_video['output']}")
    print(f"Model Used: {response_video['model']}")

if __name__ == "__main__":
    test_yuki_v06()
