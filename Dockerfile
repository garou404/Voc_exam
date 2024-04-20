FROM python:3.10
# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
#Copy files to your container
COPY . ./
#Running your APP and doing some PORT Forwarding
EXPOSE 8000

CMD ["python3", "time_spacing/app.py"]

# docker build -t image-name .

# docker volume create volume-name

# docker run -dp 127.0.0.1:8000:8000 --mount type=volume,src=volume-name,target=//path image-name