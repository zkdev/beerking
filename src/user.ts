import { RegisterUserDto } from './register-user-dto';

export class User {
  constructor(uuid: string, data: RegisterUserDto) {
    this.uuid = uuid;
    this.username = data.username;
    this.passwd = data.passwd;
    this.mail = data.mail;
  }

  uuid: string;
  username: string;
  passwd: string;
  mail: string;
}
