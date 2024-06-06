FROM node:20.14-slim

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV PORT 4242

RUN npm install -g serve

RUN npm install
RUN npm run build

CMD ["serve", "-s", "-l", "4242", "./dist"]