import streamlit as st

def render_virality_methodology():
    st.title("Viral Coefficient Methodology")
    st.markdown("### How we calculate and predict Virality")
    
    st.markdown("---")
    
    st.subheader("The Formula")
    st.latex(r"""
    \text{Viral Coefficient} = \left( \frac{5 \cdot \text{Shares} + 4 \cdot \text{Saves} + 2 \cdot \text{Comments} + 1 \cdot \text{Likes}}{\text{Views} + 1} \right) \times (1 + \text{Retention Rate}) \times (1 + \text{Growth Rate})
    """)
    
    st.markdown("""
    ### Why this specific methodology?
    
    In modern social media environments, all engagement is not created equal. 
    
    1. **Shares (Weight: 5.0)**: The highest value action. A share explicitly introduces the content to a new network, directly enabling exponential viral growth.
    2. **Saves (Weight: 4.0)**: Indicates high relatability or utility. Algorithms heavily favor Saves as a signal of high-quality content that users want to return to.
    3. **Comments (Weight: 2.0)**: Represents active engagement and community building, but doesn't guarantee distribution outside the current network.
    4. **Likes (Weight: 1.0)**: A passive action. While good for baseline engagement, it is the weakest signal of true viral potential.
    
    ### Multipliers
    * **Retention Contribution**: Content that keeps viewers watching longer signals the algorithm to push it to wider audiences. We use `(1 + Retention Rate)` as a multiplier to boost content that holds attention.
    * **Follower Growth Contribution**: If a piece of content brings in new followers, it's a strong signal of audience capture. We use normalized growth `(1 + Growth Rate)` to reward this.
    
    ### Normalization
    The final score is normalized to a 0 - 5.0 scale for readability and easier comparison across different content pieces.
    """)
    
    st.info("💡 **Note for Viva/Presentation**: This formula explicitly differentiates between vanity metrics (likes) and actual growth drivers (shares/saves), creating a much more accurate predictor of true social media success.")
