import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { InputComponent } from './input.component';

describe('InputComponent', () => {
  let component: InputComponent;
  let fixture: ComponentFixture<InputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InputComponent],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });


  it('Should set the input values on init with validation and value', () => {
    component.title = "title";
    component.regexes = { "validation": /.+/ };
    component.validator = "validation";
    component.value = "value"
    fixture.detectChanges();

    component.ngOnInit();

    expect(component.regex).toEqual(/.+/);
    expect(component.title).toBe("title  *");
  });

  it('Should set the values on input call without validation and options', () => {
    const spy = spyOn(component.childEmitter, 'emit');
    const event = { target: { value: "value" } };

    component.onInput(event);

    expect(component.isValid).toBe(true);
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith(event.target.value);
    spy.calls.reset();
  });

  it('Should set the values on input call with validation and without options', () => {
    const spy = spyOn(component.childEmitter, 'emit');
    const event = { target: { value: "value" } };
    component.validator = "validation";
    component.regex = /.+/;
    fixture.detectChanges();

    component.onInput(event);

    expect(component.isValid).toBe(true);
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith(event.target.value);
    spy.calls.reset();
  });

  it('Should set the values on input call with validation to invalid and without options', () => {
    const spy = spyOn(component.childEmitter, 'emit');
    const event = { target: { value: "value" } };
    component.validator = "validation";
    component.regex = /^([0-9]{10})$/;
    fixture.detectChanges();

    component.onInput(event);

    expect(component.isValid).toBe(false);
    expect(component.childEmitter.emit).not.toHaveBeenCalled();
    spy.calls.reset();
  });

  it('Should set focus to true if out of compoment click happens', () => {
    const event = { target: fixture.nativeElement };

    component.isFocus = true;
    fixture.detectChanges();

    component.clickout(event);

    expect(component.isFocus).toBe(true);
  });

  it('Should set focus to false if click is not out of compoment', () => {
    const event = { target: null };

    component.isFocus = true;
    fixture.detectChanges();

    component.clickout(event);

    expect(component.isFocus).toBe(false);
  });

  it('View: Should have parent tag with content css class and border style', () => {
    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.nativeElement).not.toBe(null);
    expect(content.styles['border']).toBe('1px solid var(--less-bright)');
  });
  
  it('View: Should return the red border color on invalid input', () => {
    component.isValid = false;
    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--danger)')
  });

  it('View: Should return the inactive border color on invalid input', () => {
    fixture.detectChanges();

    expect(component.isValid).not.toBeDefined()
    expect(component.getBorderColor()).toBe('var(--less-bright)')
  });

  it('View: Should return the active border color on layout is in focus', () => {
    component.isFocus = true;
    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--primary)')
  });

  it('View: Should return the inactive border color on layout is not in focus', () => {
    component.isFocus = false;
    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--less-bright)')
  });

  it('View: Should set the focus to true if on edit mode', () => {
    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.styles['border']).toBe('1px solid var(--less-bright)');

    content.nativeElement.click();
    fixture.detectChanges();

    expect(content.styles['border']).toBe('1px solid var(--primary)');
    expect(component.isFocus).toBe(true);

  });

  it('View: Should set the layout without options on edit mode', () => {
    const spy = spyOn(component, 'onInput');
    component.title = 'title';
    component.placeholder = 'placeholder';
    component.value = 'value';
    component.type = 'type';
    component.isFocus = true;
    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('.content'));
    const title = fixture.nativeElement.querySelector('span');
    const input = fixture.debugElement.query(By.css('input'));
    const optionLayout = fixture.debugElement.query(By.css('.options'));
    const optionElements = fixture.debugElement.queryAll(By.css('.option'))

    expect(content.children.length).toBe(1);
    expect(title.textContent).toBe('title');
    expect(input.nativeElement.value).toBe('value');
    expect(input.attributes['placeholder']).toBe('placeholder');
    expect(input.classes['type']).toBe(true);
    expect(optionLayout).toBeDefined();
    expect(optionElements.length).toBe(0);

    input.triggerEventHandler('input', 'sometext');

    expect(component.onInput).toHaveBeenCalledOnceWith('sometext');
    spy.calls.reset;
  });

});
