//
//  ViewController.swift
//  QuietMind
//
//  Created by Edward Arenberg on 5/5/18.
//  Copyright © 2018 Edward Arenberg. All rights reserved.
//

import UIKit
import AVFoundation
import UserNotifications

class ViewController: UIViewController {

    @IBOutlet weak var alertLabel: UILabel!
    @IBOutlet weak var alertIV: UIImageView!
    @IBOutlet weak var buttonSV: UIStackView!
    @IBOutlet weak var assistButton: UIButton! {
        didSet {
            assistButton.layer.cornerRadius = 12
            assistButton.layer.borderWidth = 2
            assistButton.layer.borderColor = UIColor.white.cgColor
        }
    }
    @IBOutlet weak var falseButton: UIButton! {
        didSet {
            falseButton.layer.cornerRadius = 12
            falseButton.layer.borderWidth = 2
            falseButton.layer.borderColor = UIColor.white.cgColor
        }
    }
    
    var pollTimer : Timer?
    var isStimming = false

    var alertSound = URL(fileURLWithPath: Bundle.main.path(forResource: "alert", ofType: "mp3")!)
    var alertPlayer : AVAudioPlayer!

    @IBAction func assistHit(_ sender: UIButton) {
        if let vc = storyboard?.instantiateViewController(withIdentifier: "ConditionVC") as? ConditionVC {
            present(vc, animated: true, completion: nil)
            showInterface(show: false)
        }
    }
    @IBAction func falseHit(_ sender: UIButton) {
        showInterface(show: false)
//        DispatchQueue.main.asyncAfter(deadline: .now()+3) { self.showInterface(show: true) }
    }
    @IBAction func activateHit(_ sender: UIButton) {
        showInterface(show: true)
    }
    
    func showInterface(show:Bool) {
        UIView.animate(withDuration: 0.4) {
            self.alertIV.alpha = show ? 1 : 0
            self.buttonSV.alpha = show ? 1 : 0
        }
        if show {
            alertPlayer.play()
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
//        showInterface(show: false)
        alertPlayer = try! AVAudioPlayer(contentsOf: alertSound)
        alertPlayer.numberOfLoops = 1
        alertPlayer.prepareToPlay()
        
        pollTimer = Timer(timeInterval: 10, repeats: true) { timer in
            return
            let u = URL(string: "https://cff47c90.ngrok.io/status?userId=0123456789")!
            let task = URLSession.shared.dataTask(with: u) { data,response,error in
//                print(error)
                guard let data = data else { print("No Data"); return }
                guard let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String:Any] else {
                    print("Parse Error")
                    if let str = String(data:data,encoding:.utf8) {
                        print(str)
                    }
                    return
                }
                if let stim = json!["status"] as? Int {
                    print("Stim = \(stim)")
                    DispatchQueue.main.async {
                        if self.isStimming {
                            if stim == 0 {
                                self.showInterface(show: false)
                                self.isStimming = false
                            }
                        } else {
                            if stim == 1 {
                                self.showInterface(show: true)
                                self.isStimming = true
                            }
                        }
                    }
                    self.isStimming = stim == 1
                }
            }
            task.resume()
        }
        RunLoop.main.add(pollTimer!, forMode: RunLoopMode.commonModes)
        
        UNUserNotificationCenter.current().getNotificationSettings { (settings) in
            print("Notification settings: \(settings)")
            if settings.authorizationStatus == .notDetermined {
                UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) {
                    (granted, error) in
                    print("Permission granted: \(granted)")
                    guard granted else {
                        return
                    }
                    DispatchQueue.main.async {
                        UIApplication.shared.registerForRemoteNotifications()
                    }
                }
            } else if settings.authorizationStatus != .authorized {
                
            } else {

            }
        }
        
        NotificationCenter.default.addObserver(forName: NSNotification.Name("AlertNotification"), object: nil, queue: .main, using: { notification in
            if let info = notification.userInfo {
                print(info)
            }
            self.showInterface(show: true)
        })

    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
//        DispatchQueue.main.asyncAfter(deadline: .now()+3) { self.showInterface(show: true) }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

