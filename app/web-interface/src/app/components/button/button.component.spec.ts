import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { ButtonComponent } from './button.component';


describe('ButtonComponent', () => {
  let componentRef: ComponentRef<ButtonComponent>;
  let fixture: ComponentFixture<ButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ButtonComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ButtonComponent);
    componentRef = fixture.componentRef;
  });

  it('Should create', () => {
    expect(componentRef).toBeTruthy();
  });

  it('View: Should have parent tag with content css class', () => {
    const content = fixture.nativeElement.querySelector('.content');

    expect(content).not.toBe(null);
  });

  it('View: Should set the parent tag with input type css class', () => {
    componentRef.setInput("type", "type");
    
    fixture.detectChanges();

    const parent = fixture.debugElement.query(By.css('.content'));
    expect(parent.classes["type"]).toBe(true);
  })

  it('View: Should set button text without icon', () => {
    componentRef.setInput("text", "text");
    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(icon).toBe(null);
    expect(title.textContent).toEqual("text");
  });

  it('View: Should set button icon and its properties without text', () => {
    componentRef.setInput("icon", "iconName");
    componentRef.setInput("iconColor", "color");
    componentRef.setInput("iconSize", 2);

    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(icon.name).toBe('iconName');
    expect(icon.size).toBe(2);
    expect(icon.fill).toBe('color');
    expect(title).toBe(null);
  });

  it('View: Should set button text with icon and its properties', () => {
    componentRef.setInput("icon", "iconName");
    componentRef.setInput("iconColor", "color");
    componentRef.setInput("iconSize", 2);
    componentRef.setInput("text", "text");

    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(title.textContent).toEqual("text");
    expect(icon.name).toBe('iconName');
    expect(icon.size).toBe(2);
    expect(icon.fill).toBe('color');
  });
});
