"""
Material Tier Simulator - Simplified version without external dependencies
Chỉ sử dụng built-in Python libraries
"""
import random
import math

class SimpleTierAnalyzer:
    """Phân tích tier distribution với built-in libraries"""
    
    def __init__(self):
        self.max_tier = 4
        self.samples = 5000  # Reduced for faster execution
    
    def simulate_old_formula(self, shrine_level: int) -> int:
        """Mô phỏng công thức TraitShrine: owner.LV / 3"""
        effective_lv = shrine_level // 3
        
        # Triple random formula: EClass.rnd(EClass.rnd(EClass.rnd(lv / 10 + 2) + 1) + 1)
        base = effective_lv // 10 + 2
        rand1 = random.randint(0, max(0, base - 1)) if base > 0 else 0
        rand2 = random.randint(0, max(0, rand1)) if rand1 > 0 else 0
        rand3 = random.randint(0, max(0, rand2)) if rand2 > 0 else 0
        
        # Apply minimum tier based on effective level
        min_tier = self.get_minimum_tier(effective_lv)
        return max(min_tier, min(rand3, self.max_tier))
    
    def simulate_exponential_formula(self, shrine_level: int) -> int:
        """Công thức exponential cải tiến"""
        effective_lv = shrine_level // 3
        normalized_level = min(effective_lv / 100.0, 1.0)
        
        # Exponential curve
        base_tier = (normalized_level ** 2) * self.max_tier
        
        # Controlled randomness
        random_factor = (random.random() - 0.5) * 1.4  # ±0.7
        final_tier = base_tier + random_factor
        
        min_tier = self.get_minimum_tier(effective_lv)
        return max(min_tier, min(round(final_tier), self.max_tier))
    
    def get_minimum_tier(self, level: int) -> int:
        """Minimum tier dựa trên level"""
        if level >= 80: return 3
        elif level >= 60: return 2  
        elif level >= 25: return 1
        return 0
    
    def analyze_shrine_levels(self, shrine_levels: list) -> dict:
        """Phân tích tier distribution cho các shrine level"""
        results = {}
        
        for shrine_lv in shrine_levels:
            print(f"Analyzing Shrine Level {shrine_lv}...")
            
            # Count tiers for old formula
            old_counts = {i: 0 for i in range(self.max_tier + 1)}
            exp_counts = {i: 0 for i in range(self.max_tier + 1)}
            
            for _ in range(self.samples):
                old_tier = self.simulate_old_formula(shrine_lv)
                exp_tier = self.simulate_exponential_formula(shrine_lv)
                
                old_counts[old_tier] += 1
                exp_counts[exp_tier] += 1
            
            # Convert to percentages
            results[shrine_lv] = {
                'old': {tier: (count/self.samples)*100 for tier, count in old_counts.items()},
                'exponential': {tier: (count/self.samples)*100 for tier, count in exp_counts.items()},
                'effective_level': shrine_lv // 3
            }
        
        return results
    
    def print_analysis_table(self, results: dict):
        """In bảng phân tích dễ đọc"""
        print("\n" + "="*80)
        print("TRAITSHRINE MATERIAL TIER DISTRIBUTION ANALYSIS")
        print("Formula: MATERIAL.GetRandomMaterial(owner.LV / 3, material_type)")
        print("="*80)
        
        for shrine_lv, data in results.items():
            effective_lv = data['effective_level']
            print(f"\nShrine Level: {shrine_lv} (Effective Level: {effective_lv})")
            print("-" * 60)
            
            # Table header
            print(f"{'Tier':<6} {'Old Formula %':<15} {'New Exponential %':<18} {'Difference':<12}")
            print("-" * 60)
            
            total_old = 0
            total_exp = 0
            
            for tier in range(self.max_tier + 1):
                old_pct = data['old'][tier]
                exp_pct = data['exponential'][tier]
                diff = exp_pct - old_pct
                
                total_old += old_pct
                total_exp += exp_pct
                
                print(f"{tier:<6} {old_pct:<15.1f} {exp_pct:<18.1f} {diff:+.1f}")
            
            # Average tier calculation
            old_avg = sum(tier * data['old'][tier] for tier in range(self.max_tier + 1)) / 100
            exp_avg = sum(tier * data['exponential'][tier] for tier in range(self.max_tier + 1)) / 100
            
            print(f"\nAverage Tier: Old={old_avg:.2f}, New={exp_avg:.2f}, Improvement={exp_avg-old_avg:+.2f}")
            
            # Material quality assessment
            high_tier_old = sum(data['old'][tier] for tier in range(3, self.max_tier + 1))
            high_tier_exp = sum(data['exponential'][tier] for tier in range(3, self.max_tier + 1))
            
            print(f"High Tier (3-4): Old={high_tier_old:.1f}%, New={high_tier_exp:.1f}%")
    
    def print_summary_recommendations(self, results: dict):
        """In tổng kết và đề xuất"""
        print("\n" + "="*80)
        print("SUMMARY & RECOMMENDATIONS")
        print("="*80)
        
        shrine_levels = list(results.keys())
        
        print("\n1. TIER PROGRESSION ANALYSIS:")
        print("   Shrine Level Range -> Primary Tiers")
        for shrine_lv in shrine_levels:
            data = results[shrine_lv]
            # Find the most common tier
            old_primary = max(data['old'].items(), key=lambda x: x[1])
            exp_primary = max(data['exponential'].items(), key=lambda x: x[1])
            
            print(f"   Level {shrine_lv:3d} -> Old: Tier {old_primary[0]} ({old_primary[1]:.1f}%), "
                  f"New: Tier {exp_primary[0]} ({exp_primary[1]:.1f}%)")
        
        print(f"\n2. BALANCING OBSERVATIONS:")
        
        # Low level analysis
        low_level = min(shrine_levels)
        low_data = results[low_level]
        low_tier0_old = low_data['old'][0]
        low_tier0_exp = low_data['exponential'][0]
        
        print(f"   Early Game (Shrine Lv {low_level}):")
        print(f"   - Old formula: {low_tier0_old:.1f}% Tier 0 (too common)")
        print(f"   - New formula: {low_tier0_exp:.1f}% Tier 0 (more balanced)")
        
        # High level analysis  
        high_level = max(shrine_levels)
        high_data = results[high_level]
        high_tier34_old = sum(high_data['old'][tier] for tier in [3, 4])
        high_tier34_exp = sum(high_data['exponential'][tier] for tier in [3, 4])
        
        print(f"   Late Game (Shrine Lv {high_level}):")
        print(f"   - Old formula: {high_tier34_old:.1f}% High Tiers (3-4)")
        print(f"   - New formula: {high_tier34_exp:.1f}% High Tiers (better progression)")
        
        print(f"\n3. IMPLEMENTATION SUGGESTIONS:")
        print(f"   - Replace triple random with exponential formula")
        print(f"   - Consider using owner.LV / 2 instead of /3 for faster progression")
        print(f"   - Add shrine type modifiers for special materials")
        print(f"   - Implement tier bonus for higher danger zones")

def main():
    """Chạy phân tích chính"""
    analyzer = SimpleTierAnalyzer()
    
    # Shrine levels thường gặp trong game
    shrine_levels = [30, 60, 90, 120, 150, 180, 240, 300]
    
    print("Material Tier Analysis for TraitShrine")
    print(f"Analyzing shrine levels: {shrine_levels}")
    print(f"Sample size: {analyzer.samples} per level")
    print("Processing...")
    
    # Chạy phân tích
    results = analyzer.analyze_shrine_levels(shrine_levels)
    
    # In kết quả
    analyzer.print_analysis_table(results)
    analyzer.print_summary_recommendations(results)
    
    print(f"\nAnalysis completed!")
    print(f"For visual charts, install matplotlib/seaborn and run tier_distribution_analyzer.py")

if __name__ == "__main__":
    main()
