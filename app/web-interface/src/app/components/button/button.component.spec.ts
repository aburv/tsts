import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { ButtonComponent } from './button.component';


describe('ButtonComponent', () => {
  let component: ButtonComponent;
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
    component = fixture.componentInstance;
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('View: Should have parent tag with content css class', () => {
    const content = fixture.nativeElement.querySelector('.content');

    expect(content).not.toBe(null);
  });

  it('View: Should set the parent tag with input type css class', () => {
    component.type = "type"
    fixture.detectChanges();

    const parent = fixture.debugElement.query(By.css('.content'));
    expect(parent.classes["type"]).toBeTruthy();
  })

  it('View: Should set button text without icon', () => {
    component.text = "text"
    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(icon).toBe(null);
    expect(title.textContent).toEqual("text");
  });

  it('View: Should set button icon and its properties without text', () => {
    component.icon = "iconName"
    component.iconColor = "color"
    component.iconSize = 2
    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(icon.name).toBe('iconName');
    expect(icon.size).toBe(2);
    expect(icon.fill).toBe('color');
    expect(title).toBe(null);
  });

  it('View: Should set button text with icon and its properties', () => {
    component.icon = "iconName"
    component.iconColor = "color"
    component.iconSize = 2
    component.text = "text"
    fixture.detectChanges();

    const title = fixture.nativeElement.querySelector('.text');
    const icon = fixture.nativeElement.querySelector('app-icon');

    expect(title.textContent).toEqual("text");
    expect(icon.name).toBe('iconName');
    expect(icon.size).toBe(2);
    expect(icon.fill).toBe('color');
  });
});
