install:
  echo "Setting up dependencies..."
  pip install -r tools/python/requirements.txt

build:
  echo "Building release..."
  python tools/python/build/create-combined-turtle.py
  python tools/python/build/create-schemas.py

check:
  echo "Running quality checks..."
  # TODO: implement quality checks

# ==============

docs:
  echo "Building docs..."
  # TODO: Run respecter to docs
