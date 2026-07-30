import streamlit.components.v1 as components


def copy_button(text, key):
    """Renders a polished icon-style copy-to-clipboard button with click feedback."""
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    components.html(f"""
        <div style="display:flex; justify-content:flex-end; margin-top:-6px;">
            <button id="btn_{key}"
                onclick="copyText_{key}()"
                title="Copy to clipboard"
                style="
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 6px;
                    cursor: pointer;
                    padding: 4px 8px;
                    font-size: 13px;
                    color: #888;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    transition: all 0.15s ease;
                "
                onmouseover="this.style.background='#f0f0f0'; this.style.color='#333'; this.style.borderColor='#ddd';"
                onmouseout="this.style.background='transparent'; this.style.color='#888'; this.style.borderColor='transparent';">
                <span id="icon_{key}">📋</span>
                <span id="label_{key}">Copy</span>
            </button>
        </div>

        <script>
            function copyText_{key}() {{
                navigator.clipboard.writeText(`{safe_text}`).then(() => {{
                    document.getElementById("icon_{key}").innerText = "✅";
                    document.getElementById("label_{key}").innerText = "Copied!";
                    setTimeout(() => {{
                        document.getElementById("icon_{key}").innerText = "📋";
                        document.getElementById("label_{key}").innerText = "Copy";
                    }}, 1500);
                }});
            }}
        </script>
    """, height=34)