import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { IconComponent } from './icon.component';

describe('IconComponent', () => {
  let component: IconComponent;
  let fixture: ComponentFixture<IconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IconComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('Should create with default icon size', () => {
    expect(component.iconSize).toBe('24');

    expect(component).toBeTruthy();
  });

  it('Should set up icon size by input size', () => {
    component.size = 20;
    fixture.detectChanges();

    component.ngOnInit();

    expect(component.iconSize).toBe('20');
  });

  it('View: Should have parent tag as svg', () => {
    const content = fixture.debugElement.query(By.css('svg'));

    expect(content.nativeElement).not.toBe(null);
    expect(content.attributes['width']).toBe('24');
    expect(content.attributes['height']).toBe('24');
    expect(content.attributes['viewBox']).toBe('0 0 24 24');

  });

  it('View: Should have parent tag as svg with input fill', () => {
    const icons = { g: [""] };
    const name = "g";

    component.icons = icons;
    component.name = name;
    component.fill = "gg";

    fixture.detectChanges();

    const paths = fixture.debugElement.queryAll(By.css('path'));
    for (let i = 0; i < paths.length; i++) {
      const pathElement = paths[i];
      expect(pathElement.attributes['d']).toBe(icons[name][i]);
      // expect(pathElement.styles['fill']).toBe("fill");
      expect(pathElement.styles['fill']).toBe("");

    }
  });

  it('View: Should have parent tag as svg with default fill', () => {
    const icons = { g: [""] };
    const name = "g";

    component.icons = icons;
    component.name = name;

    fixture.detectChanges();

    const paths = fixture.debugElement.queryAll(By.css('path'));
    for (let i = 0; i < paths.length; i++) {
      const pathElement = paths[i];
      expect(pathElement.attributes['d']).toBe(icons[name][i]);
      expect(pathElement.styles['fill']).toBe("var(--dark)");
    }
  });

});
