import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { InputComponent } from './input.component';

describe('InputComponent', () => {
  let componentRef: ComponentRef<InputComponent>;
  let component: InputComponent;
  let fixture: ComponentFixture<InputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InputComponent],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InputComponent);
    componentRef = fixture.componentRef;
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(componentRef).toBeTruthy();
  });

  it('Should set the values on input call without validation', () => {
    const spy = spyOn(component.childEmitter, 'emit');
    const event = { target: { value: "value" } };

    component.onInput(event);

    expect(component.isValid).toBe(true);
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith(event.target.value);
    spy.calls.reset();
  });

  it('Should set the values on input call with validation', () => {
    const spy = spyOn(component.childEmitter, 'emit');

    const event = { target: { value: "value" } };
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.onInput(event);

    expect(component.isValid).toBe(true);
    expect(component.childEmitter.emit).toHaveBeenCalledOnceWith(event.target.value);
    spy.calls.reset();
  });

  it('Should set the values on input call with validation to invalid', () => {
    const spy = spyOn(component.childEmitter, 'emit');
    const event = { target: { value: "value" } };
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "phone");
    componentRef.setInput('value', "value");

    component.onInput(event);

    expect(component.isValid).toBe(false);
    expect(component.childEmitter.emit).not.toHaveBeenCalled();
    spy.calls.reset();
  });

  it('Should set focus to true if out of compoment click happens', () => {
    const event = { target: fixture.nativeElement };
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.isFocus = true;

    fixture.detectChanges();
    component.clickout(event);

    expect(component.isFocus).toBe(true);
  });

  it('Should set focus to false if click is not out of compoment', () => {
    const event = { target: null };

    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.isFocus = true;

    fixture.detectChanges();
    component.clickout(event);

    expect(component.isFocus).toBe(false);
  });

  it('View: Should have parent tag with content css class and border style', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.nativeElement).not.toBe(null);
    expect(content.styles['border']).toBe('1px solid var(--less-bright)');
  });

  it('View: Should return the red border color on invalid input', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.isValid = false;

    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--danger)')
  });

  it('View: Should return the inactive border color on invalid input', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    fixture.detectChanges();

    expect(component.isValid).not.toBeDefined()
    expect(component.getBorderColor()).toBe('var(--less-bright)')
  });

  it('View: Should return the active border color on layout is in focus', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.isFocus = true;

    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--primary)')
  });

  it('View: Should return the inactive border color on layout is not in focus', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    component.isFocus = false;

    fixture.detectChanges();

    expect(component.getBorderColor()).toBe('var(--less-bright)')
  });

  it('View: Should set the focus to true if on edit mode', () => {
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");

    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('.content'));

    expect(content.styles['border']).toBe('1px solid var(--less-bright)');

    content.nativeElement.click();
    fixture.detectChanges();

    expect(content.styles['border']).toBe('1px solid var(--primary)');
    expect(component.isFocus).toBe(true);
  });

  it('View: Should set the layout on edit mode with validator', () => {
    const spy = spyOn(component, 'onInput');
    componentRef.setInput('title', "title");
    componentRef.setInput('validator', "mandatory");
    componentRef.setInput('value', "value");
    componentRef.setInput('placeholder', "placeholder");
    componentRef.setInput('type', "type");
    component.isFocus = true;

    fixture.detectChanges();

    expect(component.regex()).toEqual(/.+/);

    const content = fixture.debugElement.query(By.css('.content'));
    const title = fixture.nativeElement.querySelector('span');
    const input = fixture.debugElement.query(By.css('input'));

    expect(content.children.length).toBe(1);
    expect(title.textContent.trim()).toBe('title *');
    expect(input.nativeElement.value).toBe('value');
    expect(input.attributes['placeholder']).toBe('placeholder');
    expect(input.classes['type']).toBe(true);

    input.triggerEventHandler('input', 'sometext');

    expect(component.onInput).toHaveBeenCalledOnceWith('sometext');
    spy.calls.reset;
  });

  it('View:  Should set the layout on edit mode without validator and default type', () => {
    componentRef.setInput('title', "title");
    componentRef.setInput('value', "value");
    componentRef.setInput('placeholder', "placeholder");
    component.isFocus = true;

    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('.content'));
    const title = fixture.nativeElement.querySelector('span');
    const input = fixture.debugElement.query(By.css('input'));

    expect(content.children.length).toBe(1);
    expect(title.textContent.trim()).toBe('title');
    expect(input.nativeElement.value).toBe('value');
    expect(input.attributes['placeholder']).toBe('placeholder');
    expect(input.classes['small']).toBe(true);
  });
});
