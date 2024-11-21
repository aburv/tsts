import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { IconComponent } from './icon.component';

describe('IconComponent', () => {
  let componentRef: ComponentRef<IconComponent>;
  let fixture: ComponentFixture<IconComponent>;

  const icons: any = { g: [""] }
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IconComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IconComponent);
    IconComponent.icons = icons ;
    componentRef = fixture.componentRef;
  });

  it('View: Should have parent tag as svg with input fill, name, size', () => {
    componentRef.setInput("name", "name");
    componentRef.setInput("fill", "fill");
    componentRef.setInput("size", 20);

    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('svg'));

    expect(content.attributes['width']).toBe('20');
    expect(content.attributes['height']).toBe('20');
    expect(content.attributes['viewBox']).toBe('0 0 24 24');
    const paths = fixture.debugElement.queryAll(By.css('path'));
    for (let i = 0; i < paths.length; i++) {
      const pathElement = paths[i];
      expect(pathElement.attributes['d']).toBe(icons["name"][i]);
      expect(pathElement.styles['fill']).toBe('fill');
    }
  });

  it('View: Should have parent tag as svg with default fill and size', () => {
    componentRef.setInput("name", "name");

    fixture.detectChanges();

    const content = fixture.debugElement.query(By.css('svg'));

    expect(content.attributes['width']).toBe('24');
    expect(content.attributes['height']).toBe('24');
    expect(content.attributes['viewBox']).toBe('0 0 24 24');
    const paths = fixture.debugElement.queryAll(By.css('path'));
    for (let i = 0; i < paths.length; i++) {
      const pathElement = paths[i];
      expect(pathElement.attributes['d']).toBe(icons["name"][i]);
      expect(pathElement.styles['fill']).toBe('var(--dark)');
    }
  });

});
