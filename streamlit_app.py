# from streamlit_extras.switch_page_button import switch_page
from config.page_config import config_page

def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """

    try:
        from streamlit.runtime.scriptrunner import RerunData, RerunException
    except ModuleNotFoundError:  # For streamlit > 1.37
        from streamlit.runtime.scriptrunner_utils.exceptions import RerunException
        from streamlit.runtime.scriptrunner_utils.script_requests import RerunData

    from streamlit.runtime.pages_manager import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

config_page()
switch_page("dashboard")