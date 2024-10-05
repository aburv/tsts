import { ComponentRef, NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { TogglerComponent } from './toggler.component';

describe('TogglerComponent', () => {
  let component: TogglerComponent;
  let componentRef: ComponentRef<TogglerComponent>;
  let fixture: ComponentFixture<TogglerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TogglerComponent],
      schemas: [NO_ERRORS_SCHEMA],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TogglerComponent);
    component = fixture.componentInstance;
    componentRef = fixture.componentRef
  });

  it('Should create', () => {
    expect(component).toBeTruthy();
  });

  it('View: Should have parent tag with content css class', () => {
    const content = fixture.nativeElement.querySelector('.content');

    expect(content).not.toBe(null);
  });

  it('View: Should list the options text with item css class', () => {
    const options = ["option1", "option2"];
    const selected = "option1";

    spyOn(component.childEmitter, 'emit');
    componentRef.setInput('options', options);
    componentRef.setInput('selected', selected);
    
    fixture.detectChanges();

    const items = fixture.debugElement.queryAll(By.css('.item'));
    for (let i = 0; i < items.length; i++) {
      const itemElement = items[i].nativeElement;
      expect(itemElement.textContent).toBe(options[i]);
      if (options[i] === selected) {
        expect(items[i].classes['selected']).toBe(true);
      }
    }

    items[0].nativeElement.click();
    expect(component.childEmitter.emit).toHaveBeenCalledWith('option1');
  });
});
