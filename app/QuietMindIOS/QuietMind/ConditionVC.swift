//
//  ConditionVC.swift
//  QuietMind
//
//  Created by Edward Arenberg on 5/5/18.
//  Copyright © 2018 Edward Arenberg. All rights reserved.
//

import UIKit

class ConditionVC: UIViewController {

    enum AskState { case surroundings, behavior }
    var askState : AskState = .surroundings {
        didSet {
            switch askState {
            case .surroundings:
                break
            case .behavior:
                askLabel.text = "Behavior"
                ask1Control.setTitle("Calm", forSegmentAt: 0)
                ask1Control.setTitle("Violent", forSegmentAt: 1)
                ask1Control.selectedSegmentIndex = 0
                ask2Control.setTitle("No Damage", forSegmentAt: 0)
                ask2Control.setTitle("Damage", forSegmentAt: 1)
                ask2Control.selectedSegmentIndex = 0
                ask3Control.setTitle("Safe", forSegmentAt: 0)
                ask3Control.setTitle("Injured", forSegmentAt: 1)
                askButton.setTitle("SAVE", for: .normal)
                ask3Control.selectedSegmentIndex = 0
            }
        }
    }
    
    @IBOutlet weak var askLabel: UILabel!
    @IBOutlet weak var ask1Control: UISegmentedControl!
    @IBOutlet weak var ask2Control: UISegmentedControl!
    @IBOutlet weak var ask3Control: UISegmentedControl!
    @IBOutlet weak var askButton: UIButton! {
        didSet {
            askButton.layer.cornerRadius = 12
            askButton.layer.borderWidth = 2
            askButton.layer.borderColor = UIColor.white.cgColor
        }
    }
    
    var askResults = [Int:Int]()
    
    @IBAction func saveHit(_ sender: UIButton) {
        switch askState {
        case .surroundings:
            askState = .behavior
            askResults[0] = ask1Control.selectedSegmentIndex
            askResults[1] = ask2Control.selectedSegmentIndex
            askResults[2] = ask3Control.selectedSegmentIndex
        case .behavior:
            askResults[3] = ask1Control.selectedSegmentIndex
            askResults[4] = ask2Control.selectedSegmentIndex
            askResults[5] = ask3Control.selectedSegmentIndex
            dismiss(animated: true, completion: nil)
        }
        
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
//        let attr = NSDictionary(object: UIFont(name: "Avenir-Next-Bold", size: 24.0)!, forKey: kCTFontAttributeName as! NSCopying)
//        UISegmentedControl.appearance().setTitleTextAttributes(attr as [NSObject : AnyObject] , for: .normal)
        
//        let attr = NSDictionary(object: UIFont(name: "Avenir-Bold", size: 24.0)!, forKey: NSFontAttributeName as NSCopying)
//        UISegmentedControl.appearance().setTitleTextAttributes(attr as [NSObject : AnyObject] , for: .normal)

        let font: [AnyHashable : Any] = [NSAttributedStringKey.font : UIFont.boldSystemFont(ofSize: 24)]
        UISegmentedControl.appearance().setTitleTextAttributes(font, for: .normal)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
