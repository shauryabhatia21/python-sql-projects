from engine import AkinatorEngine

def test_character(target_name):
    e = AkinatorEngine()
    char = next((c for c in e.characters if c["name"] == target_name), None)
    assert char is not None, f"Character {target_name} not found"
    print(f"=== Testing Akinator with target: {target_name} ===")

    for step in range(15):
        q = e.get_best_question()
        if not q:
            break
        ans = char["answers"].get(q["id"], 0.5)
        e.submit_answer(q["id"], ans)
        top_c, top_p = e.get_top_candidate()
        print(f"  Step {step+1}: [{q['text']}] -> Answer: {ans} | Top: {top_c['name']} ({top_p*100:.1f}%)")
        if e.should_make_guess():
            print(f"==> GUESS: Akinator guessed '{top_c['name']}' in {step+1} questions with {top_p*100:.1f}% confidence!")
            assert top_c["name"] == target_name
            return True
    return False

if __name__ == "__main__":
    test_character("Iron Man (Tony Stark)")
    print()
    test_character("Pikachu")
    print()
    test_character("Albert Einstein")
    print()
    test_character("Doctor Strange (Stephen Strange)")
    print("\nAll engine simulation tests passed successfully!")
