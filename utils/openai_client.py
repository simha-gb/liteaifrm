import openai
from utils.secdata import get_openai_api_key


def get_client(config=None):
    """Return an initialized OpenAI client.

    Parameters
    ----------
    config : dict, optional
        Optional config that may contain ``openai_api_key`` and ``base_url``
        entries.

    Returns
    -------
    object
        Instance of :class:`openai.OpenAI` if available, otherwise the
        configured ``openai`` module.

    Raises
    ------
    RuntimeError
        If no API key could be resolved.
    """
    api_key = get_openai_api_key(config)
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Set OPENAI_API_KEY env variable or provide it via config"
        )

    base_url = None
    if config:
        base_url = config.get("base_url") or config.get("openai_base_url")

    if hasattr(openai, "OpenAI"):
        if base_url:
            return openai.OpenAI(api_key=api_key, base_url=base_url)
        return openai.OpenAI(api_key=api_key)

    # Fallback for older openai versions
    openai.api_key = api_key
    if base_url:
        if hasattr(openai, "base_url"):
            openai.base_url = base_url
        else:
            openai.api_base = base_url
    return openai
