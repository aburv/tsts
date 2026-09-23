import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DateStringType, DateTime } from './dateTime';

import { InputDateComponent } from './input-date.component';
import { By } from '@angular/platform-browser';
import { Icon } from '../icon/icon.component';

describe('InputDateComponent', () => {
  let componentRef: ComponentRef<InputDateComponent>;
  let component: InputDateComponent;
  let fixture: ComponentFixture<InputDateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InputDateComponent],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputDateComponent);
    componentRef = fixture.componentRef;
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(componentRef).toBeTruthy();
  });

  it('Should set the min, max, value value from input', () => {
    componentRef.setInput("min", new DateTime('2022-02-07'));
    componentRef.setInput("max", new DateTime('2022-02-07'));
    componentRef.setInput("value", new DateTime('2022-02-07'));

    const minSpy = spyOn(component.min()!, 'getISOString').and.returnValue('2022-02-07');
    const maxSpy = spyOn(component.max()!, 'getISOString').and.returnValue('2022-02-07');
    const valueSpy = spyOn(component.value()!, 'getISOString').and.returnValue('2022-02-07');
    const valueStringSpy = spyOn(component.value()!, 'getFormatString').and.returnValue('Jul 02, 2022');

    fixture.detectChanges();

    expect(component.min()!.getISOString).toHaveBeenCalledOnceWith();
    expect(component.minValue()).toBe('2022-02-07');

    expect(component.max()!.getISOString).toHaveBeenCalledOnceWith();
    expect(component.maxValue()).toBe('2022-02-07');

    expect(component.value()!.getISOString).toHaveBeenCalledOnceWith();
    expect(component.inputValue()).toBe('2022-02-07');

    expect(component.value()!.getISOString).toHaveBeenCalledOnceWith();
    expect(component.valueText()).toBe('Jul 02, 2022');
    minSpy.calls.reset();
    maxSpy.calls.reset();
    valueSpy.calls.reset();
    valueStringSpy.calls.reset();
  });

  it('Should set undefined for minvalue, maxvalue, inputValue, valueText on undefined', () => {
    expect(component.minValue()).toBeNull();

    expect(component.maxValue()).toBeNull();

    expect(component.inputValue()).toBeNull();

    expect(component.valueText()).toBeNull();
  });

  it('Should emit the input on notify call', () => {
    componentRef.setInput("value", new DateTime('2022-02-07'));
    spyOn(component.value()!, 'setValue')

    spyOn(component.childEmitter, 'emit');

    const event = { target: { value: '2022-07-02' } };

    component.notify(event);

    expect(component.value()!.setValue).toHaveBeenCalledOnceWith('2022-07-02');
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith('2022-07-02');
  });

  it('View: Should have parent tag with content css class and border style', () => {
    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.nativeElement).not.toBe(null);
  });

  it('View: Should set the layout without date value', () => {
    componentRef.setInput('title', 'Date');
    componentRef.setInput('value', new DateTime());

    fixture.detectChanges();

    const title = fixture.debugElement.query(By.css('.title'));
    const holder = fixture.debugElement.queryAll(By.css('.holder'));

    expect(holder.length).toBe(1);

    expect(title).toBeNull();
    expect(holder[0].nativeElement.textContent).toBe('Date');
  });

  it('View: Should set the datapicker and icon', () => {
    const spy = spyOn(component, 'notify');

    componentRef.setInput("min", new DateTime('2022-02-07', DateStringType.DATE));
    componentRef.setInput("max", new DateTime('2022-02-07'));
    componentRef.setInput("value", new DateTime('2022-02-07'));
    componentRef.setInput('title', "title");

    fixture.detectChanges();

    const layout = fixture.debugElement.query(By.css('.datepicker'));
    const icon = fixture.debugElement.query(By.css('app-icon'));
    const input = fixture.debugElement.query(By.css('input'));
    const title = fixture.debugElement.query(By.css('.title'));

    expect(layout).toBeDefined();

    expect(title.nativeElement.textContent).toBe("title");

    expect(icon.componentInstance.name()).toBe(Icon.CALENDAR);
    expect(input.attributes['max']).toBe('2022-02-07');
    expect(input.attributes['min']).toBe('2022-02-07');
    expect(input.attributes['type']).toBe('date');
    expect(input.classes['d-input']).toBe(true);

    input.triggerEventHandler('change', 'event');

    expect(component.notify).toHaveBeenCalledOnceWith('event');
    spy.calls.reset();
  });
});
