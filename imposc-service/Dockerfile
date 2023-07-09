# Use buster rather than slim-buster because we need gcc
FROM python:3.8-buster

WORKDIR /usr/src/proj

COPY . .

# Clear out any unwanted dev files from the copy
RUN rm -f /usr/src/proj/imposcpy/src/*.so

# Install Gnuplot (needed for charting)
RUN apt-get update && apt-get install -y gnuplot

# Install python dependencies
RUN cd imposcpy && python -m pip install -r requirements.txt

# Python environment
ENV PYTHONPATH=/usr/src/proj/imposcpy/src

# Build cython package
RUN cd /usr/src/proj/imposcpy/src && python setup.py build_ext --inplace

# Flask environment
ENV FLASK_APP=imposc

# Launch service
EXPOSE 4000
ENV CWD=/usr/src/proj/imposcpy/src
CMD ["gunicorn", "--bind", "localhost:4000", "--timeout", "180", "imposc:app"]
