FROM node:18-alpine

RUN mkdir -p /usr/src/node-app && chown -R node:node /usr/src/node-app

WORKDIR /usr/src/node-app

# COPY package.json  ./

COPY --chown=node:node package.json package-lock.json ./

USER node
# RUN ls
RUN npm install

COPY --chown=node:node . .

# RUN chown -R node:node /usr/src/node-app/node_modules/
# RUN chmod -R 777 /usr/src/node-app/

USER node

EXPOSE 3000

# CMD ["npm", "run","dev","--host"]