Win:
venv v\Scripts\activate

Mac:
source venv/bin/activate

deactivate

# Run

pip install -r requirements.txt

## LLaMA 2 install

model:
Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install
git clone https://huggingface.co/botato/point-alpaca-ggml-model-q4_0

if you want to clone without large files – just their pointers
prepend your git clone with the following env var:
GIT_LFS_SKIP_SMUDGE=1

mac:
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python

win:
git clone --recursive -j8 https://github.com/abetlen/llama-cpp-python.git
set FORCE_CMAKE=1
set CMAKE_ARGS=-DLLAMA_CUBLAS=OFF
python setup.py clean
python setup.py install




pip freeze > requirements.txt
