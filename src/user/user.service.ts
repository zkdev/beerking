import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import {UserDto} from "./user.dto";

@Injectable()
export class UserService {
    constructor(@InjectRepository(User) private readonly userRepository: Repository<User>) {}

    findAll(): Promise<User[]> {
        return this.userRepository.find();
    }

    findByUsername(username: string): Promise<User[]> {
        return this.userRepository.find({where: {"username": username}});
    }

    register(userDto: UserDto): Promise<User> {
        const uuidv4 = require('uuid/v4');
        const user = new User();
        user.mail = userDto.mail;
        user.passwd = userDto.passwd;
        user.username = userDto.username;
        user.uuid = uuidv4();
        return this.userRepository.manager.save(user);
    }
}
