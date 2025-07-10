import { DateStringType, DateTime } from "./dateTime";

describe('DateTime', () => {
    it('Should set the type from input', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.MONTH);

        expect(dateTime.type).toBe('month');
    });

    it('Should set the default type if input is null', () => {
        const dateTime = new DateTime('2022-12-12');

        expect(dateTime.type).toBe('date');
    });

    it('Should set the value from input', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.MONTH);

        expect(dateTime.value()).toEqual(new Date('2022-12-12'));
    });

    it('Should format the date in mmm yyyy', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.MONTH);

        expect(dateTime.getFormatString()).toBe('Dec 2022');
    });

    it('Should format the date mmm dd, yyyy', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.DATE);

        expect(dateTime.getFormatString()).toBe('Dec 12, 2022');
    });

    it('Should getISOString the date in yyyy-mm-dd', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.DATE);

        expect(dateTime.getISOString()).toBe('2022-12-12');
    });

    it('Should getISOString the date mmm, dd yyyy-mm', () => {
        const dateTime = new DateTime('2022-12-12', DateStringType.MONTH);

        expect(dateTime.getISOString()).toBe('2022-12')
    });

    it('Should getISOString the date mmm, dd yyyy-mm', () => {
        const dateTime = new DateTime('2022-02-12', DateStringType.MONTH);

        expect(dateTime.getISOString()).toBe('2022-02');
    });

    it('Should getISOString the date mmm, dd yyyy-mm', () => {
        const dateTime = new DateTime('2022-12-02', DateStringType.DATE);

        expect(dateTime.getISOString()).toBe('2022-12-02');
    });

    it('Should set value if value string is non empty string', () => {
        const dateTime = new DateTime('2022-12-02', DateStringType.DATE);

        dateTime.setValue('2022-12-12');

        expect(dateTime.value()).toEqual(new Date('2022-12-12'));
    });

    it('Should set nothing if value string is empty string', () => {
        const dateTime = new DateTime('2022-12-02', DateStringType.DATE);

        dateTime.setValue('');

        expect(dateTime.value()).toEqual(new Date('2022-12-02'));
    });

    it('Should set type', () => {
        const dateTime = new DateTime('2022-12-02', DateStringType.DATE);

        dateTime.setType(DateStringType.MONTH);

        expect(dateTime.type).toBe('month');
    });

    it('Should return true on 12-jul-1990 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1990-07-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(true);
    });

    it('Should return false on 12-Jul-1990 less than 12-Jul-1990', () => {
        const dateTime = new DateTime('1990-07-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-12', DateStringType.DATE));

        expect(actual).toBe(false);
    });

    it('Should return true on 12-jun-1990 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1990-06-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(true);
    });

    it('Should true on 12-jun-1989 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1989-07-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(true);
    });

    it('Should return false on 16-jul-1990 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1990-07-16', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(false);
    });

    it('Should return false on 12-Aug-1990 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1990-08-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(false);
    });

    it('Should return false on 12-jun-1991 less than 14-Jul-1990', () => {
        const dateTime = new DateTime('1991-07-12', DateStringType.DATE);

        const actual = dateTime.lesserThan(new DateTime('1990-07-14', DateStringType.DATE));

        expect(actual).toBe(false);
    });

    it('Should return false on null values', () => {
        const dateTime = new DateTime(null);

        const actual = dateTime.lesserThan(new DateTime(null));

        expect(actual).toBe(false);
    });

    it('Should return empty string on null value on getFormatString call', () => {
        const dateTime = new DateTime(null);

        const actual = dateTime.getFormatString();

        expect(actual).toBe("");
    });

    it('Should return empty string on null value on getISOString call', () => {
        const dateTime = new DateTime(null);

        const actual = dateTime.getISOString();

        expect(actual).toBe("");
    });
});
