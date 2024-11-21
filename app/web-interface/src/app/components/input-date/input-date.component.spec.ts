import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DateTime } from './dateTime';

import { InputDateComponent } from './input-date.component';

describe('InputDateComponent', () => {
  let componentRef: ComponentRef<InputDateComponent>;
  let fixture: ComponentFixture<InputDateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InputDateComponent],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputDateComponent);
    componentRef = fixture.componentRef;
  });

  it('Should create', () => {
    expect(componentRef).toBeTruthy();
  });

  it('Should set the min, max, value value from input', () => {
    componentRef.setInput("min", new DateTime('2022-02-07'));
    componentRef.setInput("max", new DateTime('2022-02-07'));
    componentRef.setInput("value", new DateTime('2022-02-07'));

    const minSpy = spyOn(fixture.componentInstance.min()!, 'getISOString').and.returnValue('2022-02-07');
    const maxSpy = spyOn(fixture.componentInstance.max()!, 'getISOString').and.returnValue('2022-02-07');
    const valueSpy = spyOn(fixture.componentInstance.value()!, 'getISOString').and.returnValue('2022-02-07');
    const valueStringSpy = spyOn(fixture.componentInstance.value()!, 'getFormatString').and.returnValue('Jul 02, 2022');

    fixture.detectChanges();

    expect(fixture.componentInstance.min()!.getISOString).toHaveBeenCalledOnceWith();
    expect(fixture.componentInstance.minValue()).toBe('2022-02-07');

    expect(fixture.componentInstance.max()!.getISOString).toHaveBeenCalledOnceWith();
    expect(fixture.componentInstance.maxValue()).toBe('2022-02-07');

    expect(fixture.componentInstance.value()!.getISOString).toHaveBeenCalledOnceWith();
    expect(fixture.componentInstance.inputValue()).toBe('2022-02-07');

    expect(fixture.componentInstance.value()!.getISOString).toHaveBeenCalledOnceWith();
    expect(fixture.componentInstance.valueText()).toBe('Jul 02, 2022');
    minSpy.calls.reset();
    maxSpy.calls.reset();
    valueSpy.calls.reset();
    valueStringSpy.calls.reset();
  });

  it('Should set undefined for minvalue, maxvalue, inputValue, valueText on undefined', () => {
    expect(fixture.componentInstance.minValue()).toBeNull();

    expect(fixture.componentInstance.maxValue()).toBeNull();

    expect(fixture.componentInstance.inputValue()).toBeNull();

    expect(fixture.componentInstance.valueText()).toBeNull();
  });

  it('Should emit the input on notify call', () => {
    componentRef.setInput("value", new DateTime('2022-02-07'));
    spyOn(fixture.componentInstance.value()!, 'setValue')

    spyOn(fixture.componentInstance.childEmitter, 'emit');

    const event = { target: { value: '2022-07-02' } };

    fixture.componentInstance.notify(event);

    expect(fixture.componentInstance.value()!.setValue).toHaveBeenCalledOnceWith('2022-07-02');
    expect(fixture.componentInstance.childEmitter.emit).toHaveBeenCalledOnceWith('2022-07-02');
  });

  // it('View: Should have parent tag with content css class and border style', () => {
  //   const content = fixture.debugElement.query(By.css('.content'));

  //   expect(content.nativeElement).not.toBe(null);
  // });

  // it('View: Should set the layout without date value', () => {
  //   componentRef.title = 'Date';
  //   componentRef.value = new DateTime(null, null)
  //   fixture.detectChanges();

  //   const title = fixture.debugElement.query(By.css('.title'));
  //   const holder = fixture.debugElement.queryAll(By.css('.holder'));

  //   expect(holder.length).toBe(1);

  //   expect(title).toBeNull();
  //   expect(holder[0].nativeElement.textContent).toBe('Date');

  // });

  // it('View: Should set the datapicker and icon', () => {
  //   const spy = spyOn(componentRef, 'notify');
  //   componentRef.value = new DateTime('2022-12-12', DateStringType.DATE);
  //   componentRef.maxValue = '2022-12-12';
  //   componentRef.minValue = '2022-12-12';
  //   componentRef.title = "title"

  //   fixture.detectChanges();
  //   fixture.detectChanges();

  //   const layout = fixture.debugElement.query(By.css('.datepicker'));
  //   const icon = fixture.debugElement.query(By.css('app-icon'));
  //   const input = fixture.debugElement.query(By.css('input'));
  //   const title = fixture.debugElement.query(By.css('.title'));

  //   expect(layout).toBeDefined();

  //   expect(title.nativeElement.textContent).toBe("title");

  //   expect(icon.attributes['name']).toBe('calendar');
  //   expect(input.attributes['max']).toBe('2022-12-12');
  //   expect(input.attributes['min']).toBe('2022-12-12');
  //   expect(input.attributes['type']).toBe('date');
  //   expect(input.classes['d-input']).toBe(true);

  //   input.triggerEventHandler('change', 'event');

  //   expect(componentRef.notify).toHaveBeenCalledOnceWith('event');
  //   spy.calls.reset();
  // });

});
