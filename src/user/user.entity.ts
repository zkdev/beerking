import {Entity, Column, PrimaryColumn} from "typeorm";
import {IsEmail, Length} from 'class-validator';

@Entity()
export class User {

    @PrimaryColumn()
    uuid: string;

    @Length(2, 15)
    @Column()
    username: string;

    @Length(127)
    @Column()
    passwd: string;

    @IsEmail()
    @Column()
    mail: string;

    @Column({ type: "timestamp", default: () => "CURRENT_TIMESTAMP"})
    time: string;

}
