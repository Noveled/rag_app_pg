import React, { useState } from 'react';
import Chat from './components/Chat';
import './App.css';


// Demo 버전이니까 제발 단순하게...

// Todo : 
// 0. 엔터 키로도 입력 가능하게, 추가로 입력하면 입력창 비워지게
// 1. 유저 채팅, gpt 채팅 구분 (좌우 or 이미지 사용)
// 2. gpt 채팅에 하이라이트 어떻게 넣을지 고민 필요
// 3. pdf 반환하는 경우 다운 가능하게
// 4. 페이지 두개로 나눠서 seah-bs 기능 보여주기
const App = () => {
  return (
    <div className="app-container">
      <header className="logo flex justify-between">
        <div className='flex gap-2'>
          <span>로고자리</span>
          <span>대충이쁜타이틀</span>
        </div>
        <div className="userInfo">
          <h1>대충깔끔한유저인포</h1>
        </div>
      </header>

      <div>
        <Chat />
      </div>
    </div>
  );
};

export default App;
