import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='streamlit_ws_localstorage',
    packages=setuptools.find_packages(),
    version='1.0.1',  # Ideally should be same as your GitHub release tag varsion
    description="A simple synchronous way of accessing localStorage from your Streamlit app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Gagandeep Singh',
    author_email='gagan@heloprotocol.in',
    url='https://github.com/gagangoku/streamlit-ws-localstorage',
    download_url='https://github.com/gagangoku/streamlit-ws-localstorage/archive/refs/tags/1.0.1.tar.gz',
    keywords=['python', 'websocket', 'cookies', 'localstorage', 'streamlit'],
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.86",
    ],
)
