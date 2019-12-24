import {Entity, Column, PrimaryColumn} from "typeorm";

@Entity()
export class User {

    @PrimaryColumn()
    uuid: string;

    @Column()
    username: string;

    @Column()
    passwd: string;

    @Column()
    mail: string;

    @Column({ type: "timestamp", default: () => "CURRENT_TIMESTAMP"})
    time: string;

}
