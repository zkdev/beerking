import "reflect-metadata";
import {createConnection} from "typeorm";
import {User} from "./entity/User";

createConnection({
    type: "postgres",
    host: "localhost",
    port: 5432,
    username: "postgres",
    password: "zkdev#",
    database: "postgres",
    entities: [
        User
    ],
    synchronize: true,
    logging: false
}).then(connection => {
    const uuidv4 = require('uuid/v4');
    const user = new User();
    user.mail = "dev@zeekay.dev";
    user.passwd = "kali";
    user.username = "Siggi";
    user.uuid = uuidv4();
    return connection.manager.save(user);
}).catch(error => console.log(error));
