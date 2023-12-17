import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DateTime, DateStringType } from './dateTime';

import { InputDateComponent } from './input-date.component';

describe('InputDateComponent', () => {
  let component: InputDateComponent;
  let fixture: ComponentFixture<InputDateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InputDateComponent],
      schemas: [NO_ERRORS_SCHEMA],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputDateComponent);
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('Should set the min value from input on init call', () => {
    component.min = new DateTime('2022-02-07', DateStringType.DATE);

    const spy = spyOn(component.min, 'getISOString').and.returnValue('2022-02-07');

    component.ngOnChanges();

    expect(component.min.getISOString).toHaveBeenCalledOnceWith();
    expect(component.minValue).toBe('2022-02-07');
    spy.calls.reset();
  });

  it('Should nothing set for min value on init call when no min', () => {
    component.ngOnChanges();

    expect(component.minValue).not.toBeDefined();
  });

  it('Should set the max value from input on init call', () => {
    component.max = new DateTime('2022-02-07', DateStringType.DATE);

    const spy = spyOn(component.max, 'getISOString').and.returnValue('2022-02-07');

    component.ngOnChanges();

    expect(component.max.getISOString).toHaveBeenCalledOnceWith();
    expect(component.maxValue).toBe('2022-02-07');
    spy.calls.reset();
  });

  it('Should nothing set for max value on init call when no max', () => {
    component.ngOnChanges();

    expect(component.minValue).not.toBeDefined();
  });

  it('Should set the valueText and inputValue from input on init call', () => {
    component.value = new DateTime('2022-02-07', DateStringType.DATE);

    const spy = spyOn(component.value, 'getFormatString').and.returnValue('Feb, 07 2022');
    const spyF = spyOn(component.value, 'getISOString').and.returnValue('2022-02-07');

    component.ngOnChanges();

    expect(component.value.getFormatString).toHaveBeenCalledOnceWith();
    expect(component.value.getISOString).toHaveBeenCalledOnceWith();
    expect(component.valueText).toBe('Feb, 07 2022');
    expect(component.inputValue).toBe('2022-02-07');
    spy.calls.reset();
    spyF.calls.reset();
  });

  it('Should nothing set for value text on init call when no value', () => {
    component.ngOnChanges();

    expect(component.valueText).not.toBeDefined();
    expect(component.inputValue).not.toBeDefined();
  });

  it('Should emit the input on notify call', () => {
    component.value = new DateTime('', null);
    const spyValue = spyOn(component.value, 'setValue');
    const spyFormatDate = spyOn(component.value, 'getFormatString');
    const spyGetFormatDate = spyOn(component.value, 'getISOString');

    const spy = spyOn(component.childEmitter, 'emit');

    const event = { target: { value: '2022-07-02' } };

    component.notify(event);

    expect(component.value.setValue).toHaveBeenCalledOnceWith('2022-07-02');
    spyValue.calls.reset();
    expect(component.value.getFormatString).toHaveBeenCalledOnceWith();
    spyFormatDate.calls.reset();
    expect(component.value.getISOString).toHaveBeenCalledOnceWith();
    spyGetFormatDate.calls.reset();
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith('2022-07-02');
    spy.calls.reset();
  });

  it('View: Should have parent tag with content css class and border style', () => {
    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.nativeElement).not.toBe(null);
  });

  it('View: Should set the layout without date value', () => {
    component.title = 'Date';
    component.value = new DateTime(null, null)
    fixture.detectChanges();

    const title = fixture.debugElement.query(By.css('.title'));
    const holder = fixture.debugElement.queryAll(By.css('.holder'));

    expect(holder.length).toBe(1);

    expect(title).toBeNull();
    expect(holder[0].nativeElement.textContent).toBe('Date');

  });

  it('View: Should set the datapicker and icon', () => {
    const spy = spyOn(component, 'notify');
    component.value = new DateTime('2022-12-12', DateStringType.DATE);
    component.maxValue = '2022-12-12';
    component.minValue = '2022-12-12';
    component.title = "title"

    fixture.detectChanges();
    fixture.detectChanges();

    const layout = fixture.debugElement.query(By.css('.datepicker'));
    const icon = fixture.debugElement.query(By.css('app-icon'));
    const input = fixture.debugElement.query(By.css('input'));
    const title = fixture.debugElement.query(By.css('.title'));

    expect(layout).toBeDefined();

    expect(title.nativeElement.textContent).toBe("title");

    expect(icon.attributes['name']).toBe('calendar');
    expect(input.attributes['max']).toBe('2022-12-12');
    expect(input.attributes['min']).toBe('2022-12-12');
    expect(input.attributes['type']).toBe('date');
    expect(input.classes['d-input']).toBe(true);

    input.triggerEventHandler('change', 'event');

    expect(component.notify).toHaveBeenCalledOnceWith('event');
    spy.calls.reset();
  });

});
