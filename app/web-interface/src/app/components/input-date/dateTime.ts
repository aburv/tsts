import { signal } from "@angular/core";

export enum DateStringType {
    MONTH = 'month',
    DATE = 'date'
}

export class DateTime {
    value = signal<Date | null>(null);
    type: DateStringType

    constructor(value: string | null, type: DateStringType = DateStringType.DATE) {
        if (value !== null) {
            this.value.set(new Date(value));
        }
        else {
            this.value.set(null);
        }
        this.type = type;
    }

    lesserThan(date: DateTime): boolean {
        if (this.value() !== null && date.value() !== null) {
            if (this.value()!.getFullYear() === date.value()!.getFullYear()) {
                if (this.value()!.getMonth() === date.value()!.getMonth()) {
                    if (this.value()!.getDate() < date.value()!.getDate()) {
                        return true;
                    } else {
                        return false
                    }
                } else if (this.value()!.getMonth() < date.value()!.getMonth()) {
                    return true;
                } else {
                    return false
                }
            } else if (this.value()!.getFullYear() < date.value()!.getFullYear()) {
                return true;
            } else {
                return false
            }
        }
        return false;
    }

    setValue(value: string): void {
        if (value !== '') {
            this.value.set(new Date(value));
        }
    }

    setType(type: DateStringType): void {
        this.type = type;
    }

    getFormatString(): string {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        if (this.value() !== null) {
            let value: string = ' ' + this.value()!.getFullYear();
            if (this.type === DateStringType.DATE) {
                value = ', ' + this.value()!.getDate() + value;
            }
            return months[this.value()!.getMonth()] + value;
        }
        return ""
    }

    getISOString(): string {
        if (this.value() !== null) {
            let value = this.value()!.getFullYear() + '';
            const month = this.value()!.getMonth() > 8 ? this.value()!.getMonth() + 1 : '0' + (this.value()!.getMonth() + 1);
            value += '-' + month;
            if (this.type === DateStringType.DATE) {
                const day = this.value()!.getDate() > 9 ? this.value()!.getDate() : '0' + this.value()!.getDate();
                value += '-' + day;
            }
            return value;
        }
        return ""
    }
}
