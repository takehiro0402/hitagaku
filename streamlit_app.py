import streamlit as st
import pandas as pd
import re

# ページ設定
st.set_page_config(
    page_title="日田市ゴミ分別検索",
    page_icon="🗂️",
    layout="wide"
)

# タイトル
st.title("🗂️ 日田市ゴミ分別検索")
st.markdown("---")

@st.cache_data
def load_data():
    """Excelファイルを読み込む関数"""
    try:
        df = pd.read_excel('日田市ごみ分別早見表.xlsx')
        # カラム名を確認・調整
        df.columns = df.columns.str.strip()  # 空白を削除
        return df
    except FileNotFoundError:
        st.error("Excelファイル '日田市ごみ分別早見表.xlsx' が見つかりません。")
        return None
    except Exception as e:
        st.error(f"ファイル読み込みエラー: {str(e)}")
        return None

def search_item(df, search_term):
    """品目を検索する関数"""
    if df is None or search_term.strip() == "":
        return pd.DataFrame()
    
    search_term = search_term.strip()
    
    # 完全一致検索
    exact_match = df[df['品目'].str.contains(f'^{re.escape(search_term)}$', case=False, na=False)]
    if not exact_match.empty:
        return exact_match
    
    # 部分一致検索
    partial_match = df[df['品目'].str.contains(re.escape(search_term), case=False, na=False)]
    return partial_match

def display_result(result_df):
    """検索結果を表示する関数"""
    if result_df.empty:
        st.warning("該当する品目が見つかりませんでした。")
        st.info("💡 ヒント: 品目名の一部だけでも検索できます（例：「缶」「ビン」「プラ」など）")
        return
    
    for idx, row in result_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**🏷️ 品目**")
                st.markdown(f"**♻️ 分別区分**")
                st.markdown(f"**📦 出し方**")
                if pd.notna(row.get('注意点')) and row.get('注意点').strip():
                    st.markdown(f"**⚠️ 注意点**")
            
            with col2:
                st.markdown(f"{row['品目']}")
                
                # 分別区分に応じて色を変更
                bunbetsu = row['分別区分']
                if '燃やせるごみ' in str(bunbetsu):
                    st.markdown(f'<span style="color: #ff6b6b; font-weight: bold;">{bunbetsu}</span>', unsafe_allow_html=True)
                elif '燃やせないごみ' in str(bunbetsu) or 'カナモノ' in str(bunbetsu):
                    st.markdown(f'<span style="color: #4ecdc4; font-weight: bold;">{bunbetsu}</span>', unsafe_allow_html=True)
                elif 'ビン' in str(bunbetsu) or 'ペットボトル' in str(bunbetsu):
                    st.markdown(f'<span style="color: #45b7d1; font-weight: bold;">{bunbetsu}</span>', unsafe_allow_html=True)
                elif '空き缶' in str(bunbetsu):
                    st.markdown(f'<span style="color: #96ceb4; font-weight: bold;">{bunbetsu}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f"**{bunbetsu}**")
                
                st.markdown(f"{row['出し方']}")
                
                if pd.notna(row.get('注意点')) and row.get('注意点').strip():
                    st.markdown(f"⚠️ {row['注意点']}")
            
            st.markdown("---")

# メイン処理
def main():
    # データ読み込み
    df = load_data()
    
    if df is not None:
        st.success(f"✅ データ読み込み完了 ({len(df)}件の品目データ)")
        
        # 検索インターフェース
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input(
                "🔍 ゴミの品目を入力してください",
                placeholder="例：アイロン、空き缶、ペットボトル など",
                help="品目名の一部を入力するだけでも検索できます"
            )
        
        with col2:
            search_button = st.button("検索", type="primary", use_container_width=True)
        
        # 検索実行
        if search_term or search_button:
            if search_term.strip():
                result_df = search_item(df, search_term)
                
                st.markdown("### 📋 検索結果")
                if not result_df.empty:
                    st.info(f"🎯 {len(result_df)}件の結果が見つかりました")
                
                display_result(result_df)
            else:
                st.warning("検索する品目名を入力してください。")
        
        # サンプル表示
        with st.expander("📊 データの例（最初の5件）"):
            st.dataframe(df.head(), use_container_width=True)
        
        # 使い方説明
        with st.expander("❓ 使い方"):
            st.markdown("""
            **🔍 検索方法:**
            - 捨てたいゴミの品目名を入力してください
            - 完全一致で見つからない場合は、部分一致で検索します
            - 例：「缶」と入力すると「空き缶」「缶詰」などが見つかります
            
            **📋 表示情報:**
            - **品目**: ゴミの名前
            - **分別区分**: どの種類のゴミか
            - **出し方**: どの袋に入れるか
            - **注意点**: 特別な注意事項（ある場合）
            
            **💡 検索のコツ:**
            - 品目名の一部だけでも検索できます
            - ひらがな・カタカナ・漢字どれでも検索可能です
            - 大文字・小文字は区別されません
            """)

if __name__ == "__main__":
    main()