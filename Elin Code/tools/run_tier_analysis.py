"""
Script chạy nhanh để test tier distribution
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from tier_distribution_analyzer import MaterialTierAnalyzer

def quick_analysis():
    """Phân tích nhanh với một số danger level cụ thể"""
    analyzer = MaterialTierAnalyzer()
    
    # Test levels thường gặp trong game
    test_levels = [0,30, 60, 90, 150, 240, 300]  # DLv 10, 20, 30, 50, 80, 100
    
    print("=== QUICK TIER ANALYSIS FOR TRAITSHRINE ===")
    print("Formula: owner.LV / 3")
    print()
    
    old_results = analyzer.analyze_tier_distribution(test_levels, "old")
    exp_results = analyzer.analyze_tier_distribution(test_levels, "exponential")
    
    for danger_lv in test_levels:
        effective_lv = danger_lv // 3
        print(f"Danger Level {danger_lv} (Effective: {effective_lv}):")
        
        print("  Old Formula:")
        for tier in range(5):
            print(f"    Tier {tier}: {old_results[danger_lv][tier]:.1f}%")
        
        print("  New Exponential:")
        for tier in range(5):
            print(f"    Tier {tier}: {exp_results[danger_lv][tier]:.1f}%")
        print()

if __name__ == "__main__":
    quick_analysis()
